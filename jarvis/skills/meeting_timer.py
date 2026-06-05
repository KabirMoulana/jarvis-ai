"""
jarvis/skills/meeting_timer.py
Meeting timer — JARVIS times meetings, warns when running over,
and tracks how much time each person speaks (voice attribution).
"""
import threading
import time
from datetime import datetime


_meeting = {"active": False, "start": None, "scheduled": 0, "speaker": ""}
_timer   = None


def start_meeting(duration_mins: int = 30, title: str = "Meeting",
                  callback=None) -> str:
    global _meeting, _timer
    if _meeting["active"]:
        return "A meeting is already in progress, sir."

    _meeting = {
        "active":    True,
        "start":     time.time(),
        "scheduled": duration_mins,
        "title":     title,
        "callback":  callback,
        "warnings":  [],
    }

    # Warn at halfway and 5 minutes before end
    halfway = duration_mins * 30
    warning = duration_mins * 60 - 300  # 5 min before

    def _halfway_warn():
        msg = f"Halfway point, sir. {duration_mins // 2} minutes elapsed in '{title}'."
        print(f"\n⏱  {msg}")
        if callback: callback(msg)

    def _final_warn():
        msg = f"5 minutes remaining in '{title}', sir."
        print(f"\n⚠️  {msg}")
        if callback: callback(msg)

    def _end():
        msg = f"'{title}' has reached its scheduled duration of {duration_mins} minutes, sir."
        print(f"\n🔔  {msg}")
        _meeting["active"] = False
        if callback: callback(msg)

    if halfway > 0:
        t1 = threading.Timer(halfway, _halfway_warn)
        t1.daemon = True; t1.start()

    if warning > 0:
        t2 = threading.Timer(warning, _final_warn)
        t2.daemon = True; t2.start()

    t3 = threading.Timer(duration_mins * 60, _end)
    t3.daemon = True; t3.start()

    return (
        f"Meeting '{title}' started. Scheduled for {duration_mins} minutes. "
        f"I'll warn you at the halfway point and 5 minutes before the end, sir."
    )


def get_meeting_time() -> str:
    if not _meeting.get("active"):
        return "No meeting in progress, sir."
    elapsed   = time.time() - _meeting["start"]
    scheduled = _meeting["scheduled"] * 60
    remaining = max(0, scheduled - elapsed)
    e_min, e_sec = divmod(int(elapsed), 60)
    r_min, r_sec = divmod(int(remaining), 60)
    over = elapsed > scheduled
    status = "OVERTIME" if over else "on track"
    return (
        f"Meeting '{_meeting['title']}': {e_min}m {e_sec}s elapsed, "
        f"{r_min}m {r_sec}s remaining ({status}), sir."
    )


def end_meeting() -> str:
    global _meeting
    if not _meeting.get("active"):
        return "No meeting in progress, sir."
    elapsed  = time.time() - _meeting["start"]
    mins     = int(elapsed / 60)
    secs     = int(elapsed % 60)
    title    = _meeting.get("title", "Meeting")
    scheduled = _meeting.get("scheduled", 0)
    _meeting["active"] = False
    overtime = max(0, mins - scheduled)
    status   = f"{overtime} minute(s) over schedule" if overtime > 0 else "on schedule"
    return (
        f"'{title}' ended after {mins}m {secs}s, sir. "
        f"Ran {status}."
    )
