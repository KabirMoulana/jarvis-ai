"""
jarvis/skills/password_vault.py
Password vault — JARVIS stores encrypted credentials locally.
Uses Fernet symmetric encryption. Master password required.
Requires: pip install cryptography
"""
import os
import json
import base64
import hashlib

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "vault.enc")
_SALT = b"jarvis_vault_salt_v1"


def _derive_key(master_password: str) -> bytes:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=_SALT, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def _load_vault(master_password: str) -> dict:
    if not os.path.exists(_FILE):
        return {}
    try:
        from cryptography.fernet import Fernet
        key  = _derive_key(master_password)
        f    = Fernet(key)
        with open(_FILE, "rb") as file:
            data = f.decrypt(file.read())
        return json.loads(data)
    except Exception:
        return None  # Wrong password


def _save_vault(master_password: str, vault: dict):
    from cryptography.fernet import Fernet
    key  = _derive_key(master_password)
    f    = Fernet(key)
    data = json.dumps(vault).encode()
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "wb") as file:
        file.write(f.encrypt(data))


def add_credential(site: str, username: str, password: str,
                   master_password: str) -> str:
    try:
        vault = _load_vault(master_password) or {}
        vault[site.lower()] = {"username": username, "password": password}
        _save_vault(master_password, vault)
        return f"Credentials for '{site}' saved securely, sir."
    except ImportError:
        return "cryptography not installed. Run: pip install cryptography"
    except Exception as e:
        return f"Vault error: {e}"


def get_credential(site: str, master_password: str) -> str:
    try:
        vault = _load_vault(master_password)
        if vault is None:
            return "Incorrect master password, sir."
        site_lower = site.lower()
        for key, creds in vault.items():
            if site_lower in key or key in site_lower:
                return (
                    f"Credentials for {key}, sir: "
                    f"Username: {creds['username']}, "
                    f"Password: {creds['password']}"
                )
        return f"No credentials found for '{site}', sir."
    except ImportError:
        return "cryptography not installed. Run: pip install cryptography"


def list_sites(master_password: str) -> str:
    try:
        vault = _load_vault(master_password)
        if vault is None:
            return "Incorrect master password, sir."
        if not vault:
            return "Vault is empty, sir."
        return f"Stored sites: {', '.join(vault.keys())}, sir."
    except ImportError:
        return "cryptography not installed."


def delete_credential(site: str, master_password: str) -> str:
    try:
        vault = _load_vault(master_password)
        if vault is None:
            return "Incorrect master password, sir."
        for key in list(vault.keys()):
            if site.lower() in key:
                del vault[key]
                _save_vault(master_password, vault)
                return f"Credentials for '{key}' deleted, sir."
        return f"No credentials found for '{site}', sir."
    except ImportError:
        return "cryptography not installed."
