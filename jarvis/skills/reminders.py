"""
jarvis/skills/reminders.py
Time-based reminder system — "Remind me at 3pm to call John".
Reminders persist to disk (JSON) and are reloaded on boot.
Background scheduler thread fires callbacks at the right time.
"""
import json
import os
import threading
import time
from datetime import datetime, timedelta
import re

_REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "reminders.json")
_reminders: list[dict] = []
_lock = threading.Lock()


def _load():
    global _reminders
    try:
        if os.path.exists(_REMINDERS_FILE):
            with open(_REMINDERS_FILE) as f:
                _reminders = json.load(f)
    except Exception:
        _reminders = []


def _save():
    os.makedirs(os.path.dirname(_REMINDERS_FILE), exist_ok=True)
    with open(_REMINDERS_FILE, "w") as f:
        json.dump(_reminders, f, indent=2, default=str)


def add_reminder(message: str, when: datetime, callback=None) -> str:
    """Schedule a reminder for a specific datetime."""
    with _lock:
        entry = {
            "id":      len(_reminders) + 1,
            "message": message,
            "when":    when.isoformat(),
            "fired":   False,
        }
        _reminders.append(entry)
        _save()

    delay = (when - datetime.now()).total_seconds()
    if delay > 0:
        t = threading.Timer(delay, _fire, args=(entry, callback))
        t.daemon = True
        t.start()

    time_str = when.strftime("%I:%M %p")
    return f"Reminder set for {time_str}, sir. I'll remind you to {message}."


def _fire(entry: dict, callback=None):
    msg = f"Sir, reminder: {entry['message']}."
    with _lock:
        entry["fired"] = True
        _save()
    print(f"\n🔔  {msg}")
    if callback:
        callback(msg)


def list_reminders() -> str:
    _load()
    pending = [r for r in _reminders if not r["fired"]]
    if not pending:
        return "No pending reminders, sir."
    lines = []
    for r in pending:
        when = datetime.fromisoformat(r["when"]).strftime("%I:%M %p")
        lines.append(f"{r['id']}. {r['message']} at {when}")
    return "Your reminders: " + "; ".join(lines) + "."


def clear_reminders() -> str:
    global _reminders
    with _lock:
        _reminders = []
        _save()
    return "All reminders cleared, sir."


def parse_reminder(text: str) -> tuple[str, datetime | None]:
    """
    Parse 'remind me at 3pm to call John' or 'remind me in 2 hours to check email'.
    Returns (message, datetime) or (message, None) on parse failure.
    """
    # "remind me in X minutes/hours to <msg>"
    m = re.search(r"remind\s+me\s+in\s+(\d+)\s*(minute|hour|second)s?\s+(?:to\s+)?(.+)", text, re.I)
    if m:
        amount, unit, msg = int(m.group(1)), m.group(2).lower(), m.group(3).strip()
        delta = {"minute": 60, "hour": 3600, "second": 1}.get(unit, 60) * amount
        return msg, datetime.now() + timedelta(seconds=delta)

    # "remind me at 3pm / 15:30 to <msg>"
    m = re.search(r"remind\s+me\s+at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s+(?:to\s+)?(.+)", text, re.I)
    if m:
        hour, minute, ampm, msg = m.group(1), m.group(2) or "00", m.group(3), m.group(4).strip()
        hour = int(hour); minute = int(minute)
        if ampm:
            if ampm.lower() == "pm" and hour != 12: hour += 12
            if ampm.lower() == "am" and hour == 12: hour = 0
        now   = datetime.now()
        when  = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if when < now:
            when += timedelta(days=1)
        return msg, when

    return text, None


# Load persisted reminders on import
_load()
