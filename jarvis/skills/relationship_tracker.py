"""
jarvis/skills/relationship_tracker.py
Relationship tracker — JARVIS helps maintain connections
by tracking when you last spoke to people and sending reminders.
"""
import json
import os
from datetime import date, datetime, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "relationships.json")


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(data: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def add_person(name: str, relationship: str = "friend",
               check_in_days: int = 30) -> str:
    data = _load()
    entry = {
        "name":           name.strip(),
        "relationship":   relationship.lower(),
        "check_in_days":  check_in_days,
        "last_contact":   str(date.today()),
        "notes":          [],
    }
    data.append(entry)
    _save(data)
    return (
        f"'{name}' added as {relationship}, sir. "
        f"I'll remind you to check in every {check_in_days} days."
    )


def log_contact(name: str, note: str = "") -> str:
    data = _load()
    for p in data:
        if name.lower() in p["name"].lower():
            p["last_contact"] = str(date.today())
            if note:
                p["notes"].append({"date": str(date.today()), "note": note})
            _save(data)
            return f"Contact with '{p['name']}' logged today, sir."
    return f"'{name}' not found, sir. Add them first."


def get_overdue_contacts() -> str:
    data  = _load()
    today = date.today()
    overdue = []
    for p in data:
        last    = date.fromisoformat(p["last_contact"])
        days    = (today - last).days
        if days >= p["check_in_days"]:
            overdue.append(f"{p['name']} ({days} days ago)")
    if not overdue:
        return "All relationships up to date, sir. You're doing well."
    return (
        f"{len(overdue)} relationship(s) need attention, sir: "
        + " | ".join(overdue) + "."
    )


def get_relationship_stats() -> str:
    data  = _load()
    today = date.today()
    if not data:
        return "No relationships tracked, sir."
    avg_days = sum(
        (today - date.fromisoformat(p["last_contact"])).days
        for p in data
    ) / len(data)
    types    = {}
    for p in data:
        types[p["relationship"]] = types.get(p["relationship"], 0) + 1
    type_str = ", ".join(f"{v} {k}(s)" for k, v in types.items())
    return (
        f"Relationship tracker, sir: {len(data)} connections — {type_str}. "
        f"Average days since last contact: {avg_days:.0f}."
    )


def add_note(name: str, note: str) -> str:
    data = _load()
    for p in data:
        if name.lower() in p["name"].lower():
            p["notes"].append({"date": str(date.today()), "note": note})
            _save(data)
            return f"Note added for '{p['name']}', sir."
    return f"'{name}' not found, sir."
