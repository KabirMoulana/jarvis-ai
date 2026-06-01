"""
jarvis/skills/focus_mode.py
Focus mode — Iron Man style productivity lock.
Blocks distracting sites via /etc/hosts, sets a Pomodoro timer,
and gives JARVIS-style status updates throughout the session.
"""
import os
import threading
import time
from datetime import datetime, timedelta

_HOSTS_FILE    = "/etc/hosts"
_HOSTS_MARKER  = "# JARVIS FOCUS MODE"
_DEFAULT_SITES = [
    "twitter.com", "www.twitter.com",
    "x.com", "www.x.com",
    "instagram.com", "www.instagram.com",
    "reddit.com", "www.reddit.com",
    "youtube.com", "www.youtube.com",
    "facebook.com", "www.facebook.com",
    "tiktok.com", "www.tiktok.com",
]

_active_session: dict = {}


def start_focus(minutes: int = 25, callback=None) -> str:
    """
    Start a focus session. Blocks distracting sites and starts a Pomodoro timer.
    Requires sudo for /etc/hosts modification.
    """
    global _active_session
    if _active_session.get("active"):
        remaining = _get_remaining()
        return f"Focus session already active, sir. {remaining} remaining."

    end_time = datetime.now() + timedelta(minutes=minutes)
    _active_session = {"active": True, "end": end_time, "minutes": minutes}

    _block_sites()

    def _finish():
        time.sleep(minutes * 60)
        _unblock_sites()
        _active_session["active"] = False
        msg = (
            f"Focus session complete, sir. "
            f"You've worked for {minutes} minutes. Time for a 5-minute break."
        )
        print(f"\n🎯  {msg}")
        if callback:
            callback(msg)

    t = threading.Thread(target=_finish, daemon=True)
    t.start()

    return (
        f"Focus mode activated for {minutes} minutes, sir. "
        f"Distracting sites blocked. I'll notify you when the session ends."
    )


def stop_focus() -> str:
    global _active_session
    if not _active_session.get("active"):
        return "No active focus session, sir."
    _unblock_sites()
    _active_session["active"] = False
    return "Focus mode deactivated. Sites unblocked, sir."


def focus_status() -> str:
    if not _active_session.get("active"):
        return "No focus session running, sir."
    return f"Focus session active. {_get_remaining()} remaining."


def _get_remaining() -> str:
    end = _active_session.get("end")
    if not end:
        return "unknown time"
    delta = int((end - datetime.now()).total_seconds())
    if delta <= 0:
        return "0 minutes"
    m, s = divmod(delta, 60)
    return f"{m} minutes {s} seconds"


def _block_sites() -> None:
    try:
        lines = []
        if os.path.exists(_HOSTS_FILE):
            with open(_HOSTS_FILE) as f:
                lines = f.readlines()
        # Remove any existing JARVIS block
        lines = [l for l in lines if _HOSTS_MARKER not in l]
        lines.append(f"\n{_HOSTS_MARKER} START\n")
        for site in _DEFAULT_SITES:
            lines.append(f"127.0.0.1  {site}  {_HOSTS_MARKER}\n")
        lines.append(f"{_HOSTS_MARKER} END\n")
        with open(_HOSTS_FILE, "w") as f:
            f.writelines(lines)
    except PermissionError:
        pass  # Requires sudo — fails silently, timer still works
    except Exception:
        pass


def _unblock_sites() -> None:
    try:
        if not os.path.exists(_HOSTS_FILE):
            return
        with open(_HOSTS_FILE) as f:
            lines = f.readlines()
        lines = [l for l in lines if _HOSTS_MARKER not in l]
        with open(_HOSTS_FILE, "w") as f:
            f.writelines(lines)
    except Exception:
        pass
