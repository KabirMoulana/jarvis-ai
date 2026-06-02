"""
jarvis/skills/alarm.py
Alarm system — set, list, cancel alarms by time of day.
Alarms persist across sessions via JSON.
Fires a spoken alert and plays a system beep when triggered.
"""
import json
import os
import threading
import time
from datetime import datetime, timedelta

_ALARMS_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "alarms.json")
_alarms: list[dict] = []
_threads: dict[str, threading.Timer] = {}
_lock = threading.Lock()


def _load():
    global _alarms
    try:
        if os.path.exists(_ALARMS_FILE):
            with open(_ALARMS_FILE) as f:
                _alarms = json.load(f)
    except Exception:
        _alarms = []


def _save():
    os.makedirs(os.path.dirname(_ALARMS_FILE), exist_ok=True)
    with open(_ALARMS_FILE, "w") as f:
        json.dump(_alarms, f, indent=2, default=str)


def set_alarm(hour: int, minute: int, label: str = "alarm", callback=None) -> str:
    """Set an alarm for a specific time today (or tomorrow if time has passed)."""
    now  = datetime.now()
    when = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if when <= now:
        when += timedelta(days=1)

    with _lock:
        entry = {
            "id":    len(_alarms) + 1,
            "label": label,
            "when":  when.isoformat(),
            "fired": False,
        }
        _alarms.append(entry)
        _save()

    delay = (when - datetime.now()).total_seconds()
    t = threading.Timer(delay, _fire, args=(entry, callback))
    t.daemon = True
    t.start()
    _threads[str(entry["id"])] = t

    time_str = when.strftime("%I:%M %p")
    return f"Alarm set for {time_str}, sir." + (f" Label: {label}." if label != "alarm" else "")


def _fire(entry: dict, callback=None):
    msg = f"Sir, your {entry['label']} alarm is going off."
    with _lock:
        entry["fired"] = True
        _save()
    # System beep
    print(f"\n🔔🔔🔔  {msg}  🔔🔔🔔\n")
    try:
        import sys
        sys.stdout.write("\a"); sys.stdout.flush()
    except Exception:
        pass
    if callback:
        callback(msg)


def cancel_alarm(alarm_id: int | None = None) -> str:
    """Cancel an alarm by ID, or the next upcoming one."""
    with _lock:
        pending = [a for a in _alarms if not a["fired"]]
        if not pending:
            return "No active alarms to cancel, sir."
        target = next((a for a in pending if a["id"] == alarm_id), pending[0])
        target["fired"] = True
        _save()
        t = _threads.pop(str(target["id"]), None)
        if t:
            t.cancel()
    when = datetime.fromisoformat(target["when"]).strftime("%I:%M %p")
    return f"Alarm for {when} cancelled, sir."


def list_alarms() -> str:
    _load()
    pending = [a for a in _alarms if not a["fired"]]
    if not pending:
        return "No active alarms, sir."
    lines = []
    for a in pending:
        when = datetime.fromisoformat(a["when"]).strftime("%I:%M %p")
        lines.append(f"{a['id']}. {a['label']} at {when}")
    return f"{len(pending)} active alarm(s), sir: " + "; ".join(lines) + "."


def parse_alarm_time(text: str) -> tuple[int, int, str]:
    """
    Parse 'set alarm for 7am', 'wake me up at 6:30', 'alarm at 8pm'.
    Returns (hour, minute, label).
    """
    import re
    m = re.search(r"(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text, re.I)
    if m:
        hour   = int(m.group(1))
        minute = int(m.group(2) or 0)
        ampm   = (m.group(3) or "").lower()
        if ampm == "pm" and hour != 12: hour += 12
        if ampm == "am" and hour == 12: hour  = 0
        label_m = re.search(r"label(?:led)?\s+(.+)|(?:called|named)\s+(.+)", text, re.I)
        label   = (label_m.group(1) or label_m.group(2)).strip() if label_m else "alarm"
        return hour, minute, label
    return 7, 0, "alarm"


_load()
