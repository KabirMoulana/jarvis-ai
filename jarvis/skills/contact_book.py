"""
jarvis/skills/contact_book.py
Contact book — JARVIS stores and retrieves contact information.
Supports add, search, update, delete, and quick dial.
"""
import json
import os
import re

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "contacts.json")


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(contacts: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


def add_contact(name: str, phone: str = "", email: str = "", note: str = "") -> str:
    contacts = _load()
    # Check for duplicate
    for c in contacts:
        if c["name"].lower() == name.lower():
            return f"Contact '{name}' already exists, sir. Say 'update contact {name}' to modify."
    contact = {
        "id":    len(contacts) + 1,
        "name":  name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "note":  note.strip(),
    }
    contacts.append(contact)
    _save(contacts)
    return f"Contact '{name}' saved, sir."


def find_contact(query: str) -> str:
    contacts = _load()
    query    = query.lower().strip()
    matches  = [c for c in contacts if query in c["name"].lower()
                or query in c.get("phone", "")
                or query in c.get("email", "").lower()]
    if not matches:
        return f"No contact found for '{query}', sir."
    results = []
    for c in matches[:3]:
        parts = [c["name"]]
        if c.get("phone"): parts.append(c["phone"])
        if c.get("email"): parts.append(c["email"])
        results.append(", ".join(parts))
    return ". ".join(results) + "."


def delete_contact(name: str) -> str:
    contacts = _load()
    before   = len(contacts)
    contacts = [c for c in contacts if name.lower() not in c["name"].lower()]
    if len(contacts) < before:
        _save(contacts)
        return f"Contact '{name}' deleted, sir."
    return f"No contact named '{name}' found, sir."


def list_contacts() -> str:
    contacts = _load()
    if not contacts:
        return "No contacts saved yet, sir. Say 'add contact [name]' to start."
    names = ", ".join(c["name"] for c in contacts[:10])
    total = len(contacts)
    return f"You have {total} contact(s), sir: {names}" + ("..." if total > 10 else ".") 


def call_contact(name: str) -> str:
    """Open phone dialer for a contact (macOS FaceTime / tel: URL)."""
    contacts = _load()
    for c in contacts:
        if name.lower() in c["name"].lower():
            phone = c.get("phone", "")
            if not phone:
                return f"{c['name']} has no phone number saved, sir."
            import subprocess, sys, urllib.parse
            if sys.platform == "darwin":
                subprocess.Popen(["open", f"tel:{phone}"])
                return f"Calling {c['name']} at {phone}, sir."
            return f"{c['name']}'s number is {phone}, sir."
    return f"No contact named '{name}', sir."
