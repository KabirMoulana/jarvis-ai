"""
jarvis/skills/daily_planner.py
Daily planner — JARVIS helps structure your day with
time-blocked schedules, priorities, and end-of-day reviews.
"""
import json
import os
from datetime import datetime, date, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "planner.json")

_TIME_BLOCKS = {
    "morning":   (6, 12),
    "afternoon": (12, 17),
    "evening":   (17, 21),
    "night":     (21, 24),
}


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def plan_day(tasks: list[str], date_str: str = "") -> str:
    """Add tasks to today's plan."""
    data    = _load()
    day_key = date_str or str(date.today())
    if day_key not in data:
        data[day_key] = {"tasks": [], "completed": []}
    for task in tasks:
        data[day_key]["tasks"].append({"task": task, "done": False, "time": ""})
    _save(data)
    return f"Added {len(tasks)} task(s) to your plan for {day_key}, sir."


def add_task_with_time(task: str, time_str: str) -> str:
    """Add a time-blocked task to today's plan."""
    data    = _load()
    day_key = str(date.today())
    if day_key not in data:
        data[day_key] = {"tasks": [], "completed": []}
    data[day_key]["tasks"].append({"task": task, "done": False, "time": time_str})
    _save(data)
    return f"Added '{task}' at {time_str} to today's plan, sir."


def get_today_plan() -> str:
    data    = _load()
    day_key = str(date.today())
    if day_key not in data or not data[day_key]["tasks"]:
        return "No plan for today, sir. Say 'plan my day' to add tasks."
    tasks    = data[day_key]["tasks"]
    pending  = [t for t in tasks if not t["done"]]
    done     = [t for t in tasks if t["done"]]
    parts    = []
    if pending:
        parts.append("Pending: " + ", ".join(
            f"{t['time']} {t['task']}" if t.get("time") else t["task"]
            for t in pending
        ))
    if done:
        parts.append(f"Completed: {len(done)} task(s)")
    return f"Today's plan ({len(tasks)} tasks): " + " | ".join(parts) + ", sir."


def complete_task(task_name: str) -> str:
    data    = _load()
    day_key = str(date.today())
    if day_key not in data:
        return "No plan for today, sir."
    for t in data[day_key]["tasks"]:
        if task_name.lower() in t["task"].lower():
            t["done"] = True
            _save(data)
            return f"'{t['task']}' marked complete, sir."
    return f"Task '{task_name}' not found in today's plan, sir."


def end_of_day_review() -> str:
    data    = _load()
    day_key = str(date.today())
    if day_key not in data:
        return "No plan found for today, sir."
    tasks   = data[day_key]["tasks"]
    done    = sum(1 for t in tasks if t["done"])
    pending = len(tasks) - done
    pct     = int(done / len(tasks) * 100) if tasks else 0
    rating  = "excellent" if pct >= 80 else "good" if pct >= 60 else "fair" if pct >= 40 else "let's do better tomorrow"
    return (
        f"End of day review, sir. "
        f"Tasks completed: {done}/{len(tasks)} ({pct}%) — {rating}. "
        f"{pending} task(s) carry over to tomorrow."
    )
