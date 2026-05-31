"""
jarvis/skills/timer.py
Timer and alarm skill — set countdowns by voice.
Runs each timer in a background thread so Jarvis stays responsive.
The callback speaks aloud when the timer fires.
"""
import threading
import time
from datetime import datetime, timedelta


# holds active timers: name → threading.Timer
_active: dict[str, threading.Timer] = {}


def set_timer(seconds: int, label: str = "timer", callback=None) -> str:
    """
    Start a countdown timer.
    callback(label) is called when it fires; defaults to a print.
    Returns a confirmation string.
    """
    if seconds <= 0:
        return "Timer duration must be greater than zero, sir."

    name = f"{label}_{int(time.time())}"

    def _fire():
        _active.pop(name, None)
        msg = f"Sir, your {label} is done." if label != "timer" else "Timer complete, sir."
        if callback:
            callback(msg)
        else:
            print(f"\n⏰  {msg}")

    t = threading.Timer(seconds, _fire)
    t.daemon = True
    t.start()
    _active[name] = t

    human = _human_duration(seconds)
    return f"{label.capitalize()} set for {human}, sir."


def cancel_timer(label: str = "") -> str:
    """Cancel the most recent timer (or one matching label)."""
    if not _active:
        return "No active timers to cancel, sir."
    # cancel the last started one if no label given
    key = None
    if label:
        for k in reversed(list(_active.keys())):
            if label.lower() in k.lower():
                key = k
                break
    if key is None:
        key = list(_active.keys())[-1]

    t = _active.pop(key, None)
    if t:
        t.cancel()
        return f"Timer '{key.split('_')[0]}' cancelled, sir."
    return "Could not find that timer."


def list_timers() -> str:
    """Return the number of active timers."""
    if not _active:
        return "No active timers, sir."
    names = [k.split("_")[0] for k in _active]
    return f"{len(_active)} active timer(s): {', '.join(names)}."


def parse_duration(text: str) -> int:
    """
    Parse a natural-language duration like '5 minutes', '90 seconds',
    '2 hours 30 minutes' into total seconds. Returns 0 on failure.
    """
    import re
    total = 0
    patterns = [
        (r"(\d+)\s*hour",   3600),
        (r"(\d+)\s*min",    60),
        (r"(\d+)\s*sec",    1),
    ]
    for pattern, multiplier in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            total += int(m.group(1)) * multiplier
    return total


def _human_duration(seconds: int) -> str:
    parts = []
    h, rem = divmod(seconds, 3600)
    m, s   = divmod(rem, 60)
    if h: parts.append(f"{h} hour{'s' if h > 1 else ''}")
    if m: parts.append(f"{m} minute{'s' if m > 1 else ''}")
    if s: parts.append(f"{s} second{'s' if s > 1 else ''}")
    return " ".join(parts) or "0 seconds"
