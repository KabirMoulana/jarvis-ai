"""
jarvis/skills/password_gen.py
Secure password and passphrase generator — JARVIS style.
Generates strong passwords, passphrases, PINs and copies to clipboard.
"""
import random
import string
import secrets
import subprocess
import sys

_WORDLIST = [
    "alpha", "bravo", "charlie", "delta", "echo", "falcon", "gamma",
    "hotel", "india", "jarvis", "kilo", "lima", "mike", "nova",
    "omega", "pepper", "quantum", "romeo", "sierra", "tango",
    "ultra", "victor", "whiskey", "xray", "yankee", "zulu",
    "stark", "shield", "avenger", "reactor", "armor", "repulsor",
    "thunder", "lightning", "shadow", "falcon", "spider", "rhodey",
    "nexus", "cipher", "vector", "photon", "neutron", "quasar",
]


def generate_password(length: int = 16, include_symbols: bool = True) -> str:
    """Generate a cryptographically secure random password."""
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*"

    while True:
        pwd = "".join(secrets.choice(chars) for _ in range(length))
        # Ensure at least one of each required type
        has_upper  = any(c.isupper()  for c in pwd)
        has_lower  = any(c.islower()  for c in pwd)
        has_digit  = any(c.isdigit()  for c in pwd)
        has_symbol = any(c in "!@#$%^&*" for c in pwd) or not include_symbols
        if has_upper and has_lower and has_digit and has_symbol:
            break

    _copy_to_clipboard(pwd)
    return (
        f"Generated a {length}-character password and copied it to your clipboard, sir. "
        f"Store it securely."
    )


def generate_passphrase(words: int = 4) -> str:
    """Generate a memorable passphrase from random words."""
    chosen = [secrets.choice(_WORDLIST) for _ in range(words)]
    number = secrets.randbelow(9000) + 1000
    phrase = "-".join(chosen) + f"-{number}"
    _copy_to_clipboard(phrase)
    return (
        f"Generated a {words}-word passphrase and copied it to your clipboard, sir. "
        f"It's memorable yet secure."
    )


def generate_pin(digits: int = 6) -> str:
    """Generate a secure numeric PIN."""
    pin = "".join(str(secrets.randbelow(10)) for _ in range(digits))
    _copy_to_clipboard(pin)
    return f"Generated a {digits}-digit PIN and copied it to your clipboard, sir."


def check_password_strength(password: str) -> str:
    """Rate the strength of a given password."""
    score = 0
    feedback = []

    if len(password) >= 8:  score += 1
    else: feedback.append("too short (use 8+ characters)")

    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1

    if any(c.isupper() for c in password): score += 1
    else: feedback.append("add uppercase letters")

    if any(c.islower() for c in password): score += 1
    else: feedback.append("add lowercase letters")

    if any(c.isdigit() for c in password): score += 1
    else: feedback.append("add numbers")

    if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password): score += 1
    else: feedback.append("add special characters")

    rating = {7: "excellent", 6: "strong", 5: "good", 4: "fair", 3: "weak"}.get(score, "very weak")
    tip = f" Suggestions: {', '.join(feedback)}." if feedback else " Well done, sir."
    return f"Password strength: {rating} ({score}/7).{tip}"


def _copy_to_clipboard(text: str):
    try:
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif sys.platform == "win32":
            subprocess.run(["clip"], input=text.encode(), check=True)
        else:
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=text.encode(), check=True)
    except Exception:
        pass
