"""
jarvis/skills/sleep_tracker.py
Sleep tracker — JARVIS logs your sleep, wakes, and quality.
Calculates sleep debt and trends over the week.
"""
import json
import os
from datetime import date, datetime, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "sleep.json")


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


def log_sleep(bedtime_hour: int, bedtime_min: int,
              wake_hour: int, wake_min: int,
              quality: int = 3) -> str:
    """Log a sleep session. quality 1-5."""
    data   = _load()
    bed    = datetime.now().replace(hour=bedtime_hour, minute=bedtime_min, second=0)
    wake   = datetime.now().replace(hour=wake_hour,   minute=wake_min,    second=0)
    if wake < bed:
        wake += timedelta(days=1)
    hours  = (wake - bed).total_seconds() / 3600
    entry  = {
        "date":    str(date.today()),
        "bed":     f"{bedtime_hour:02d}:{bedtime_min:02d}",
        "wake":    f"{wake_hour:02d}:{wake_min:02d}",
        "hours":   round(hours, 1),
        "quality": max(1, min(5, quality)),
    }
    data.append(entry)
    _save(data)
    rating  = "excellent" if hours >= 8 else "good" if hours >= 7 else "fair" if hours >= 6 else "insufficient"
    stars   = "★" * entry["quality"] + "☆" * (5 - entry["quality"])
    return (
        f"Sleep logged, sir. {hours:.1f} hours ({rating}). "
        f"Quality: {stars}."
    )


def get_sleep_summary() -> str:
    data = _load()
    if not data:
        return "No sleep data logged yet, sir."
    recent = data[-7:]
    avg_h  = sum(e["hours"] for e in recent) / len(recent)
    avg_q  = sum(e["quality"] for e in recent) / len(recent)
    debt   = max(0, (8 - avg_h) * len(recent))
    trend  = "improving" if len(recent) > 1 and recent[-1]["hours"] > recent[0]["hours"] else "stable"
    return (
        f"Sleep summary (last {len(recent)} nights), sir: "
        f"average {avg_h:.1f} hours, quality {avg_q:.1f}/5. "
        f"Sleep debt: {debt:.1f} hours. Trend: {trend}."
    )


def get_last_night() -> str:
    data = _load()
    if not data:
        return "No sleep data, sir."
    e = data[-1]
    return (
        f"Last night: {e['hours']} hours "
        f"({e['bed']} to {e['wake']}), "
        f"quality {e['quality']}/5, sir."
    )
