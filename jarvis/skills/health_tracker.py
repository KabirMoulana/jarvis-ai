"""
jarvis/skills/health_tracker.py
Health & wellness tracker — JARVIS monitors your habits.
Tracks: water intake, steps (manual), posture reminders,
eye break reminders (20-20-20 rule), and daily summaries.
Data persists to JSON.
"""
import json
import os
import threading
from datetime import datetime, date

_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "health.json")


def _load() -> dict:
    today = str(date.today())
    try:
        if os.path.exists(_DATA_FILE):
            with open(_DATA_FILE) as f:
                data = json.load(f)
            if data.get("date") == today:
                return data
    except Exception:
        pass
    return {
        "date":          today,
        "water_ml":      0,
        "steps":         0,
        "eye_breaks":    0,
        "posture_checks": 0,
    }


def _save(data: dict):
    os.makedirs(os.path.dirname(_DATA_FILE), exist_ok=True)
    with open(_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Water ──────────────────────────────────────────────────────────────────────

def log_water(ml: int = 250) -> str:
    data = _load()
    data["water_ml"] += ml
    _save(data)
    total  = data["water_ml"]
    goal   = 2000
    pct    = min(int(total / goal * 100), 100)
    status = "Goal reached!" if total >= goal else f"{goal - total}ml remaining to hit your daily goal."
    return f"Logged {ml}ml of water, sir. Total today: {total}ml ({pct}%). {status}"


def water_status() -> str:
    data  = _load()
    total = data["water_ml"]
    goal  = 2000
    return f"You've had {total}ml of water today, sir. Daily goal is {goal}ml."


# ── Steps ──────────────────────────────────────────────────────────────────────

def log_steps(steps: int) -> str:
    data = _load()
    data["steps"] += steps
    _save(data)
    total = data["steps"]
    goal  = 10000
    return f"Logged {steps} steps. Total today: {total} of {goal} goal, sir."


# ── Eye break (20-20-20 rule) ──────────────────────────────────────────────────

def start_eye_break_reminders(interval_mins: int = 20, callback=None) -> str:
    """Remind every 20 minutes to look 20 feet away for 20 seconds."""
    def _remind():
        while True:
            threading.Event().wait(interval_mins * 60)
            data = _load()
            data["eye_breaks"] += 1
            _save(data)
            msg = (
                "Sir, time for an eye break. "
                "Look at something 20 feet away for 20 seconds. "
                "Your eyes will thank you."
            )
            print(f"\n👁️  {msg}")
            if callback:
                callback(msg)

    t = threading.Thread(target=_remind, daemon=True)
    t.start()
    return f"Eye break reminders set every {interval_mins} minutes, sir. 20-20-20 rule activated."


# ── Posture ────────────────────────────────────────────────────────────────────

def start_posture_reminders(interval_mins: int = 30, callback=None) -> str:
    def _remind():
        while True:
            threading.Event().wait(interval_mins * 60)
            data = _load()
            data["posture_checks"] += 1
            _save(data)
            msg = "Posture check, sir. Sit up straight. Shoulders back."
            print(f"\n🪑  {msg}")
            if callback:
                callback(msg)

    t = threading.Thread(target=_remind, daemon=True)
    t.start()
    return f"Posture reminders activated every {interval_mins} minutes, sir."


# ── Daily summary ──────────────────────────────────────────────────────────────

def daily_health_summary() -> str:
    data = _load()
    return (
        f"Health summary for today, sir. "
        f"Water: {data['water_ml']}ml. "
        f"Steps: {data['steps']}. "
        f"Eye breaks taken: {data['eye_breaks']}. "
        f"Posture checks: {data['posture_checks']}."
    )
