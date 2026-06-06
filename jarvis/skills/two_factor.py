"""
jarvis/skills/two_factor.py
Two-factor authentication helper — JARVIS generates
TOTP codes for your 2FA accounts (like Google Authenticator).
Requires: pip install pyotp
"""
import json
import os
import time

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "totp_accounts.json")


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_account(name: str, secret: str) -> str:
    """Add a TOTP account. secret is the base32 key from the QR code."""
    data = _load()
    data[name.lower()] = secret.upper().strip().replace(" ", "")
    _save(data)
    return f"2FA account '{name}' added, sir. Your codes are stored securely."


def get_code(account: str) -> str:
    """Get the current TOTP code for an account."""
    try:
        import pyotp
    except ImportError:
        return "pyotp not installed. Run: pip install pyotp"

    data    = _load()
    account = account.lower().strip()
    secret  = None

    for key, val in data.items():
        if account in key or key in account:
            secret = val
            account = key
            break

    if not secret:
        accounts = ", ".join(data.keys()) if data else "none"
        return f"Account '{account}' not found, sir. Saved accounts: {accounts}."

    try:
        totp      = pyotp.TOTP(secret)
        code      = totp.now()
        remaining = 30 - (int(time.time()) % 30)
        return (
            f"2FA code for {account}: {code}. "
            f"Valid for {remaining} more seconds, sir."
        )
    except Exception as e:
        return f"Could not generate code: {e}"


def list_accounts() -> str:
    data = _load()
    if not data:
        return "No 2FA accounts saved, sir."
    return f"Saved 2FA accounts: {', '.join(data.keys())}, sir."


def remove_account(name: str) -> str:
    data = _load()
    key  = name.lower()
    for k in list(data.keys()):
        if key in k or k in key:
            del data[k]
            _save(data)
            return f"Account '{k}' removed, sir."
    return f"Account '{name}' not found, sir."


def generate_secret() -> str:
    """Generate a new TOTP secret for testing."""
    try:
        import pyotp
        secret = pyotp.random_base32()
        return f"Generated TOTP secret: {secret}. Store this securely, sir."
    except ImportError:
        return "pyotp not installed. Run: pip install pyotp"
