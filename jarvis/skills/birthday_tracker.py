"""
jarvis/skills/birthday_tracker.py
Birthday tracker — JARVIS remembers birthdays and reminds you.
Checks on boot and speaks upcoming birthdays.
"""
import json
import os
from datetime import date, datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "birthdays.json")


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
        json.dump(data, f, indent=2)


def add_birthday(name: str, month: int, day: int, year: int = 0) -> str:
    data = _load()
    entry = {
        "name":  name.strip(),
        "month": month,
        "day":   day,
        "year":  year,
    }
    data.append(entry)
    _save(data)
    month_name = datetime(2000, month, day).strftime("%B %d")
    return f"Birthday saved for {name} on {month_name}, sir."


def get_upcoming_birthdays(days_ahead: int = 7) -> str:
    data  = _load()
    today = date.today()
    upcoming = []

    for b in data:
        try:
            bday = date(today.year, b["month"], b["day"])
            if bday < today:
                bday = date(today.year + 1, b["month"], b["day"])
            diff = (bday - today).days
            if diff <= days_ahead:
                upcoming.append((diff, b["name"], bday))
        except Exception:
            pass

    if not upcoming:
        return f"No birthdays in the next {days_ahead} days, sir."

    upcoming.sort()
    parts = []
    for diff, name, bday in upcoming:
        if diff == 0:
            parts.append(f"Today is {name}'s birthday!")
        elif diff == 1:
            parts.append(f"{name}'s birthday is tomorrow")
        else:
            parts.append(f"{name}'s birthday is in {diff} days ({bday.strftime('%B %d')})")

    return " | ".join(parts) + ", sir."


def check_today_birthdays() -> str:
    data  = _load()
    today = date.today()
    bdays = [b["name"] for b in data
             if b["month"] == today.month and b["day"] == today.day]
    if not bdays:
        return ""
    names = ", ".join(bdays)
    return f"Sir, today is {names}'s birthday! Don't forget to send your wishes."


def list_birthdays() -> str:
    data = _load()
    if not data:
        return "No birthdays saved, sir."
    parts = [f"{b['name']} — {datetime(2000, b['month'], b['day']).strftime('%B %d')}"
             for b in sorted(data, key=lambda x: (x["month"], x["day"]))]
    return f"Saved birthdays: " + ", ".join(parts) + ", sir."


def remove_birthday(name: str) -> str:
    data   = _load()
    before = len(data)
    data   = [b for b in data if name.lower() not in b["name"].lower()]
    if len(data) < before:
        _save(data)
        return f"Birthday for '{name}' removed, sir."
    return f"No birthday found for '{name}', sir."
