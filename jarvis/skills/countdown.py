"""
jarvis/skills/countdown.py
Event countdown — JARVIS counts down to important dates.
Birthdays, holidays, deadlines, launches — anything with a date.
"""
import json
import os
from datetime import datetime, date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "countdowns.json")


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


def add_countdown(name: str, target_date: str) -> str:
    """Add a countdown. target_date format: YYYY-MM-DD"""
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        return f"Invalid date format, sir. Use YYYY-MM-DD."
    data = _load()
    data.append({"name": name, "date": target_date})
    _save(data)
    days = (target - date.today()).days
    if days < 0:
        return f"'{name}' was {abs(days)} days ago, sir."
    return f"Countdown to '{name}' added. {days} days to go, sir."


def get_countdowns() -> str:
    data  = _load()
    today = date.today()
    if not data:
        return "No countdowns set, sir."
    parts = []
    for c in sorted(data, key=lambda x: x["date"]):
        target = datetime.strptime(c["date"], "%Y-%m-%d").date()
        days   = (target - today).days
        if days == 0:
            parts.append(f"Today is {c['name']}!")
        elif days > 0:
            parts.append(f"{c['name']}: {days} days")
        else:
            parts.append(f"{c['name']}: {abs(days)} days ago")
    return "Countdowns: " + " | ".join(parts) + ", sir."


def remove_countdown(name: str) -> str:
    data   = _load()
    before = len(data)
    data   = [c for c in data if name.lower() not in c["name"].lower()]
    if len(data) < before:
        _save(data)
        return f"Countdown '{name}' removed, sir."
    return f"No countdown named '{name}', sir."


def days_until(target_date: str) -> str:
    """Quick one-off days until a date."""
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
        days   = (target - date.today()).days
        if days == 0: return "That's today, sir."
        if days < 0:  return f"That was {abs(days)} days ago, sir."
        return f"{days} days until {target.strftime('%B %d, %Y')}, sir."
    except ValueError:
        return "Invalid date format, sir. Use YYYY-MM-DD."
