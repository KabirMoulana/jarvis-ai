"""
jarvis/skills/study_timer.py
Study timer — JARVIS times study sessions, tracks subject hours,
and gives focus/break recommendations based on session length.
"""
import time
import threading
import json
import os
from datetime import date, datetime

_FILE     = os.path.join(os.path.dirname(__file__), "..", "memory", "study_log.json")
_session  = {"active": False, "subject": "", "start": None}
_timer    = None


def start_study(subject: str = "general", callback=None) -> str:
    global _session
    if _session["active"]:
        return f"Already studying {_session['subject']}, sir."
    _session = {"active": True, "subject": subject, "start": time.time(), "callback": callback}
    return f"Study session started for '{subject}', sir. I'll track your time."


def stop_study() -> str:
    global _session
    if not _session["active"]:
        return "No active study session, sir."
    elapsed  = time.time() - _session["start"]
    mins     = int(elapsed / 60)
    subject  = _session["subject"]
    _session["active"] = False
    _log_session(subject, mins)
    advice = _get_advice(mins)
    return f"Study session ended. {mins} minutes on '{subject}'. {advice}"


def _log_session(subject: str, minutes: int):
    try:
        data = {}
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                data = json.load(f)
        today = str(date.today())
        if today not in data:
            data[today] = {}
        data[today][subject] = data[today].get(subject, 0) + minutes
        os.makedirs(os.path.dirname(_FILE), exist_ok=True)
        with open(_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def get_study_stats(days: int = 7) -> str:
    try:
        if not os.path.exists(_FILE):
            return "No study sessions logged yet, sir."
        with open(_FILE) as f:
            data = json.load(f)
        total   = sum(
            mins for day_data in data.values()
            for mins in day_data.values()
        )
        today_data = data.get(str(date.today()), {})
        today_mins = sum(today_data.values())
        subjects   = {}
        for day_data in data.values():
            for subj, mins in day_data.items():
                subjects[subj] = subjects.get(subj, 0) + mins
        top = max(subjects, key=subjects.get) if subjects else "none"
        return (
            f"Study stats, sir: {today_mins} minutes today. "
            f"Total: {total} minutes logged. "
            f"Most studied: {top} ({subjects.get(top, 0)} minutes)."
        )
    except Exception as e:
        return f"Could not load stats: {e}"


def _get_advice(minutes: int) -> str:
    if minutes < 25:
        return "Short session. Consider a Pomodoro (25 min) next time, sir."
    elif minutes < 50:
        return "Good session. Take a 5-minute break, sir."
    elif minutes < 90:
        return "Solid work. Time for a 15-minute break, sir."
    else:
        return "Extended session. Rest well — you've earned it, sir."
