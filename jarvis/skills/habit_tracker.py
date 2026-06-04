"""
jarvis/skills/habit_tracker.py
Habit tracking — JARVIS tracks your daily habits and streaks.
Log habits, view streaks, get motivational nudges.
"""
import json
import os
from datetime import date, datetime, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "habits.json")


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
        json.dump(data, f, indent=2)


def add_habit(name: str) -> str:
    data = _load()
    key  = name.lower().strip()
    if key in data:
        return f"Habit '{name}' already exists, sir."
    data[key] = {"name": name, "log": [], "created": str(date.today())}
    _save(data)
    return f"Habit '{name}' added, sir. I'll track your streak daily."


def log_habit(name: str) -> str:
    data   = _load()
    key    = name.lower().strip()
    today  = str(date.today())

    # Fuzzy match
    matched_key = None
    for k in data:
        if name.lower() in k or k in name.lower():
            matched_key = k
            break
    if not matched_key:
        return f"Habit '{name}' not found, sir. Add it first."

    habit = data[matched_key]
    if today in habit["log"]:
        streak = _calculate_streak(habit["log"])
        return f"'{habit['name']}' already logged today, sir. Current streak: {streak} day(s)."

    habit["log"].append(today)
    _save(data)
    streak = _calculate_streak(habit["log"])
    msg    = f"'{habit['name']}' logged for today, sir. Streak: {streak} day(s)."
    if streak > 0 and streak % 7 == 0:
        msg += f" Impressive — {streak // 7} week(s) straight!"
    return msg


def get_habits_summary() -> str:
    data = _load()
    if not data:
        return "No habits tracked yet, sir. Say 'add habit exercise' to start."
    today  = str(date.today())
    parts  = []
    for key, habit in data.items():
        streak  = _calculate_streak(habit["log"])
        done    = today in habit["log"]
        status  = "✓" if done else "✗"
        parts.append(f"{status} {habit['name']}: {streak}d streak")
    return "Habit summary, sir — " + ", ".join(parts) + "."


def remove_habit(name: str) -> str:
    data = _load()
    key  = name.lower().strip()
    for k in list(data.keys()):
        if name.lower() in k or k in name.lower():
            del data[k]
            _save(data)
            return f"Habit '{name}' removed, sir."
    return f"Habit '{name}' not found, sir."


def _calculate_streak(log: list[str]) -> int:
    if not log:
        return 0
    dates  = sorted(set(log), reverse=True)
    today  = date.today()
    streak = 0
    check  = today
    for d in dates:
        if str(check) == d:
            streak += 1
            check  -= timedelta(days=1)
        elif str(check - timedelta(days=1)) == d:
            streak += 1
            check  -= timedelta(days=2)
        else:
            break
    return streak
