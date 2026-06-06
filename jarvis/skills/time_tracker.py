"""
jarvis/skills/time_tracker.py
Time tracker — JARVIS tracks time spent on projects,
generates timesheets, and calculates billable hours.
"""
import json
import os
import time
from datetime import datetime, date, timedelta

_FILE    = os.path.join(os.path.dirname(__file__), "..", "memory", "time_log.json")
_active  = {}


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


def start_timer(project: str) -> str:
    """Start tracking time for a project."""
    if project in _active:
        elapsed = time.time() - _active[project]["start"]
        return (
            f"Already tracking '{project}' for "
            f"{int(elapsed/60)} minutes, sir."
        )
    _active[project] = {"start": time.time(), "project": project}
    return f"Timer started for '{project}', sir."


def stop_timer(project: str) -> str:
    """Stop tracking time for a project."""
    if project not in _active:
        # Fuzzy match
        for key in _active:
            if project.lower() in key.lower():
                project = key
                break
    if project not in _active:
        return f"No active timer for '{project}', sir."

    elapsed = time.time() - _active[project]["start"]
    minutes = int(elapsed / 60)
    hours   = elapsed / 3600

    data   = _load()
    entry  = {
        "project": project,
        "date":    str(date.today()),
        "start":   datetime.fromtimestamp(_active[project]["start"]).isoformat(),
        "end":     datetime.now().isoformat(),
        "minutes": minutes,
        "hours":   round(hours, 2),
    }
    data.append(entry)
    _save(data)
    del _active[project]

    return (
        f"Timer stopped for '{project}', sir. "
        f"Duration: {minutes} minutes ({hours:.2f} hours)."
    )


def get_active_timers() -> str:
    if not _active:
        return "No active timers, sir."
    parts = []
    for project, info in _active.items():
        elapsed = int((time.time() - info["start"]) / 60)
        parts.append(f"'{project}': {elapsed} minutes")
    return "Active timers: " + " | ".join(parts) + ", sir."


def get_timesheet(days: int = 7) -> str:
    """Get a timesheet summary for the past N days."""
    data   = _load()
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    recent = [e for e in data if e["date"] >= cutoff]

    if not recent:
        return f"No time logged in the past {days} days, sir."

    by_project: dict[str, float] = {}
    for e in recent:
        by_project[e["project"]] = by_project.get(e["project"], 0) + e["hours"]

    total  = sum(by_project.values())
    parts  = [f"{proj}: {hrs:.1f}h" for proj, hrs in
              sorted(by_project.items(), key=lambda x: x[1], reverse=True)]
    return (
        f"Timesheet (last {days} days): "
        f"Total {total:.1f} hours. "
        + " | ".join(parts) + ", sir."
    )


def get_billable_amount(hourly_rate: float, days: int = 30) -> str:
    """Calculate billable amount at given rate."""
    data   = _load()
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    recent = [e for e in data if e["date"] >= cutoff]
    total_hours = sum(e["hours"] for e in recent)
    amount      = total_hours * hourly_rate
    return (
        f"Billable amount (last {days} days): "
        f"{total_hours:.1f} hours × ${hourly_rate:.2f}/hr = ${amount:,.2f}, sir."
    )
