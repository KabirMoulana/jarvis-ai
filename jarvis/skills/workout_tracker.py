"""
jarvis/skills/workout_tracker.py
Workout tracker — JARVIS logs workouts, tracks sets/reps,
and gives encouragement. Stores history in JSON.
"""
import json
import os
from datetime import date, datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "workouts.json")

_EXERCISES = {
    "push up": {"muscles": "chest, triceps", "type": "bodyweight"},
    "pull up": {"muscles": "back, biceps",   "type": "bodyweight"},
    "squat":   {"muscles": "legs, glutes",   "type": "bodyweight"},
    "plank":   {"muscles": "core",           "type": "bodyweight"},
    "deadlift":{"muscles": "back, legs",     "type": "barbell"},
    "bench press":{"muscles": "chest",       "type": "barbell"},
    "run":     {"muscles": "cardio",         "type": "cardio"},
}


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


def log_exercise(exercise: str, sets: int = 0, reps: int = 0,
                 weight_kg: float = 0, duration_mins: int = 0) -> str:
    data  = _load()
    entry = {
        "date":     str(date.today()),
        "time":     datetime.now().strftime("%H:%M"),
        "exercise": exercise.lower(),
        "sets":     sets,
        "reps":     reps,
        "weight":   weight_kg,
        "duration": duration_mins,
    }
    data.append(entry)
    _save(data)

    details = []
    if sets and reps: details.append(f"{sets} sets of {reps} reps")
    if weight_kg:     details.append(f"{weight_kg}kg")
    if duration_mins: details.append(f"{duration_mins} minutes")
    detail_str = " — " + ", ".join(details) if details else ""
    return f"Logged {exercise}{detail_str}, sir. Keep it up."


def get_today_workout() -> str:
    data  = _load()
    today = str(date.today())
    exercises = [e for e in data if e["date"] == today]
    if not exercises:
        return "No workout logged today, sir. Let's fix that."
    parts = []
    for e in exercises:
        s = e["exercise"]
        if e["sets"]: s += f" {e['sets']}x{e['reps']}"
        if e["weight"]: s += f" @{e['weight']}kg"
        parts.append(s)
    return f"Today's workout — {len(exercises)} exercise(s): " + ", ".join(parts) + ", sir."


def get_workout_streak() -> str:
    data  = _load()
    dates = sorted(set(e["date"] for e in data), reverse=True)
    if not dates:
        return "No workouts logged yet, sir."
    streak = 1
    for i in range(1, len(dates)):
        from datetime import timedelta
        d1 = date.fromisoformat(dates[i-1])
        d2 = date.fromisoformat(dates[i])
        if (d1 - d2).days == 1:
            streak += 1
        else:
            break
    return f"Workout streak: {streak} day(s), sir. {'Impressive!' if streak >= 7 else 'Keep going!'}"


def get_exercise_info(exercise: str) -> str:
    exercise = exercise.lower().strip()
    for name, info in _EXERCISES.items():
        if exercise in name or name in exercise:
            return f"{name.title()}: targets {info['muscles']}, type: {info['type']}, sir."
    return f"Exercise '{exercise}' not in database, sir. Log it anyway with 'log exercise {exercise}'."
