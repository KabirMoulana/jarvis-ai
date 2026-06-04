"""
jarvis/skills/pomodoro.py
Pomodoro technique — JARVIS runs structured work/break cycles
with spoken announcements and session tracking.
"""
import threading
import time
import json
import os
from datetime import date

_FILE      = os.path.join(os.path.dirname(__file__), "..", "memory", "pomodoro.json")
_session   = {"active": False, "round": 0, "work_mins": 25, "break_mins": 5}
_timer     = None


def start_pomodoro(work_mins: int = 25, break_mins: int = 5,
                   long_break_mins: int = 15, callback=None) -> str:
    global _session, _timer
    if _session["active"]:
        return f"Pomodoro already running, sir. Round {_session['round']}."

    _session = {
        "active":    True,
        "round":     1,
        "work_mins": work_mins,
        "break_mins": break_mins,
        "long_break": long_break_mins,
        "callback":  callback,
    }
    _run_cycle()
    return (
        f"Pomodoro started, sir. {work_mins}-minute work session. "
        f"I'll notify you when it's time for a break."
    )


def _run_cycle():
    global _timer, _session
    if not _session["active"]:
        return

    r        = _session["round"]
    work     = _session["work_mins"]
    brk      = _session["long_break"] if r % 4 == 0 else _session["break_mins"]
    callback = _session.get("callback")

    def _work_done():
        _log_round()
        msg = (
            f"Work session {r} complete, sir. "
            f"{'Long break time — {brk} minutes.' if r % 4 == 0 else f'Take a {brk}-minute break.'}"
        )
        print(f"\n🍅  {msg}")
        if callback: callback(msg)
        _timer = threading.Timer(brk * 60, _break_done)
        _timer.daemon = True
        _timer.start()

    def _break_done():
        _session["round"] += 1
        msg = f"Break over, sir. Starting work session {_session['round']}."
        print(f"\n💪  {msg}")
        if callback: callback(msg)
        _run_cycle()

    global _timer
    _timer = threading.Timer(work * 60, _work_done)
    _timer.daemon = True
    _timer.start()


def stop_pomodoro() -> str:
    global _session, _timer
    if _timer:
        _timer.cancel()
    completed = _session.get("round", 1) - 1
    _session["active"] = False
    return f"Pomodoro stopped, sir. Completed {completed} session(s) today."


def get_pomodoro_status() -> str:
    if not _session.get("active"):
        stats = _get_today_stats()
        return f"No active Pomodoro, sir. {stats}"
    return f"Pomodoro active — round {_session['round']}, {_session['work_mins']}-minute sessions, sir."


def _log_round():
    try:
        data = {}
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                data = json.load(f)
        today = str(date.today())
        data[today] = data.get(today, 0) + 1
        os.makedirs(os.path.dirname(_FILE), exist_ok=True)
        with open(_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def _get_today_stats() -> str:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                data = json.load(f)
            today = str(date.today())
            count = data.get(today, 0)
            return f"You've completed {count} Pomodoro(s) today, sir."
    except Exception:
        pass
    return "No Pomodoro sessions logged today, sir."
