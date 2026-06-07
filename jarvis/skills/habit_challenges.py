"""
jarvis/skills/habit_challenges.py
30-day habit challenges — JARVIS guides you through
structured monthly improvement challenges.
"""
import json
import os
from datetime import date, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "challenges.json")

_CHALLENGES = {
    "fitness": {
        "name":        "30-Day Fitness Challenge",
        "description": "Build a daily exercise habit from scratch.",
        "tasks": {
            1: "10 push-ups", 2: "15 push-ups + 10 squats",
            3: "20 push-ups + 15 squats + 1-min plank",
            7: "50 push-ups + 30 squats + 2-min plank",
            14: "100 push-ups + 50 squats + 3-min plank",
            21: "150 push-ups + 75 squats + 4-min plank",
            30: "200 push-ups + 100 squats + 5-min plank",
        },
    },
    "reading": {
        "name":        "30-Day Reading Challenge",
        "description": "Read for 20 minutes every day.",
        "tasks": {i: f"Read for 20 minutes (Day {i})" for i in range(1, 31)},
    },
    "journaling": {
        "name":        "30-Day Journaling Challenge",
        "description": "Write something every day.",
        "tasks": {
            1: "Write 3 things you're grateful for",
            2: "Describe your perfect day",
            3: "Write about your biggest goal",
            7: "What have you learned this week?",
            14: "Write a letter to your future self",
            21: "What would you do if you couldn't fail?",
            30: "Reflect on the past 30 days",
        },
    },
    "coding": {
        "name":        "30-Day Coding Challenge",
        "description": "Code something every day.",
        "tasks": {
            1:  "Build a hello world in a new language",
            3:  "Create a simple calculator",
            7:  "Build a to-do list CLI app",
            14: "Create a web scraper",
            21: "Build a REST API",
            30: "Deploy a project to the internet",
        },
    },
    "no sugar": {
        "name":        "30-Day No Sugar Challenge",
        "description": "Eliminate added sugars for 30 days.",
        "tasks": {i: f"No added sugar — Day {i} of 30" for i in range(1, 31)},
    },
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


def start_challenge(challenge_name: str) -> str:
    data      = _load()
    name      = challenge_name.lower()
    challenge = None
    for key in _CHALLENGES:
        if name in key or key in name:
            challenge = _CHALLENGES[key]
            name      = key
            break
    if not challenge:
        available = ", ".join(_CHALLENGES.keys())
        return f"Challenge '{challenge_name}' not found, sir. Available: {available}."

    data[name] = {
        "started":   str(date.today()),
        "completed": [],
        "active":    True,
    }
    _save(data)
    today_task = challenge["tasks"].get(1, "Begin the challenge")
    return (
        f"'{challenge['name']}' started, sir! "
        f"Day 1 task: {today_task}. "
        f"I'll track your progress for 30 days."
    )


def get_todays_task(challenge_name: str) -> str:
    data      = _load()
    name      = challenge_name.lower()
    challenge = None
    for key in _CHALLENGES:
        if name in key or key in name:
            challenge = _CHALLENGES[key]
            name      = key
            break
    if not challenge or name not in data:
        return f"No active '{challenge_name}' challenge, sir. Say 'start challenge {challenge_name}'."

    started = date.fromisoformat(data[name]["started"])
    day     = (date.today() - started).days + 1
    if day > 30:
        return f"30-day '{challenge['name']}' complete! Outstanding, sir."

    task = challenge["tasks"].get(day)
    if not task:
        # Find nearest defined task
        available_days = sorted(k for k in challenge["tasks"].keys() if k <= day)
        task = challenge["tasks"].get(available_days[-1], f"Continue day {day}") if available_days else f"Day {day}"

    return f"Day {day}/30 — {challenge['name']}: {task}, sir."


def complete_day(challenge_name: str) -> str:
    data = _load()
    name = challenge_name.lower()
    for key in list(data.keys()):
        if name in key or key in name:
            today = str(date.today())
            if today not in data[key]["completed"]:
                data[key]["completed"].append(today)
                _save(data)
                streak = len(data[key]["completed"])
                return f"Day {streak} complete! Keep going, sir."
    return f"Challenge '{challenge_name}' not found, sir."
