"""
jarvis/skills/home_automation_scheduler.py
Home automation scheduler — schedule smart home actions
at specific times or on recurring schedules.
"""
import threading
import time
import json
import os
from datetime import datetime, timedelta

_FILE      = os.path.join(os.path.dirname(__file__), "..", "memory", "home_schedule.json")
_schedules = []
_lock      = threading.Lock()


def _load():
    global _schedules
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                _schedules = json.load(f)
    except Exception:
        _schedules = []


def _save():
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(_schedules, f, indent=2, default=str)


def schedule_action(device: str, action: str, time_str: str,
                    repeat: str = "once", callback=None) -> str:
    """
    Schedule a home automation action.
    time_str: 'HH:MM' format
    repeat: 'once', 'daily', 'weekdays', 'weekends'
    """
    try:
        hour, minute = map(int, time_str.split(":"))
    except ValueError:
        return f"Invalid time format, sir. Use HH:MM (e.g. 07:30)."

    with _lock:
        entry = {
            "id":      len(_schedules) + 1,
            "device":  device,
            "action":  action,
            "time":    time_str,
            "repeat":  repeat,
            "active":  True,
        }
        _schedules.append(entry)
        _save()

    _start_schedule_thread(entry, callback)
    return (
        f"Scheduled: {action} {device} at {time_str} "
        f"({repeat}), sir."
    )


def _start_schedule_thread(entry: dict, callback=None):
    def _run():
        while entry.get("active"):
            now    = datetime.now()
            target = now.replace(
                hour=int(entry["time"].split(":")[0]),
                minute=int(entry["time"].split(":")[1]),
                second=0, microsecond=0
            )
            if target <= now:
                target += timedelta(days=1)

            weekday = target.weekday()
            repeat  = entry.get("repeat", "once")
            if repeat == "weekdays" and weekday >= 5:
                time.sleep(60); continue
            if repeat == "weekends" and weekday < 5:
                time.sleep(60); continue

            delay = (target - datetime.now()).total_seconds()
            time.sleep(max(0, delay))

            from jarvis.skills.smart_home import turn_on, turn_off
            if entry["action"] == "on":
                result = turn_on(entry["device"])
            else:
                result = turn_off(entry["device"])

            msg = f"Scheduled action: {entry['action']} {entry['device']} — {result}"
            print(f"\n🏠  {msg}")
            if callback: callback(msg)

            if repeat == "once":
                entry["active"] = False
                break

    t = threading.Thread(target=_run, daemon=True)
    t.start()


def list_schedules() -> str:
    _load()
    active = [s for s in _schedules if s.get("active")]
    if not active:
        return "No active home automation schedules, sir."
    parts = [
        f"{s['id']}. {s['action']} {s['device']} at {s['time']} ({s['repeat']})"
        for s in active
    ]
    return f"{len(active)} schedule(s): " + " | ".join(parts) + ", sir."


def cancel_schedule(schedule_id: int) -> str:
    _load()
    for s in _schedules:
        if s["id"] == schedule_id:
            s["active"] = False
            _save()
            return f"Schedule {schedule_id} cancelled, sir."
    return f"Schedule {schedule_id} not found, sir."


_load()
