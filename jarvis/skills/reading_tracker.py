"""
jarvis/skills/reading_tracker.py
Reading tracker — JARVIS tracks reading sessions, pages read,
reading speed, and annual reading goals.
"""
import json
import os
from datetime import date, datetime, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "reading.json")


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"sessions": [], "goal": 12, "year": date.today().year}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def log_reading(book: str, pages: int, minutes: int = 0) -> str:
    data = _load()
    wpm  = int((pages * 250) / minutes) if minutes > 0 else 0
    entry = {
        "book":    book.strip(),
        "pages":   pages,
        "minutes": minutes,
        "wpm":     wpm,
        "date":    str(date.today()),
    }
    data["sessions"].append(entry)
    _save(data)
    speed_str = f" Reading speed: ~{wpm} WPM." if wpm else ""
    return f"Logged {pages} pages of '{book}', sir.{speed_str}"


def get_reading_stats() -> str:
    data     = _load()
    sessions = data["sessions"]
    if not sessions:
        return "No reading sessions logged yet, sir."

    total_pages  = sum(s["pages"] for s in sessions)
    total_mins   = sum(s["minutes"] for s in sessions if s["minutes"])
    books        = list(dict.fromkeys(s["book"] for s in sessions))
    this_year    = [s for s in sessions if s["date"].startswith(str(date.today().year))]
    year_pages   = sum(s["pages"] for s in this_year)
    goal         = data.get("goal", 12)

    avg_wpm = 0
    wpm_sessions = [s["wpm"] for s in sessions if s["wpm"]]
    if wpm_sessions:
        avg_wpm = int(sum(wpm_sessions) / len(wpm_sessions))

    return (
        f"Reading stats, sir: {total_pages:,} pages across {len(books)} book(s). "
        f"This year: {year_pages:,} pages. "
        f"Annual book goal: {len(set(s['book'] for s in this_year))}/{goal}. "
        + (f"Average reading speed: ~{avg_wpm} WPM." if avg_wpm else "")
    )


def set_annual_goal(books: int) -> str:
    data = _load()
    data["goal"] = books
    _save(data)
    return f"Annual reading goal set to {books} books, sir."


def get_reading_streak() -> str:
    data    = _load()
    sessions = data["sessions"]
    if not sessions:
        return "No reading sessions yet, sir."
    dates  = sorted(set(s["date"] for s in sessions), reverse=True)
    streak = 1
    for i in range(1, len(dates)):
        d1 = date.fromisoformat(dates[i-1])
        d2 = date.fromisoformat(dates[i])
        if (d1 - d2).days == 1:
            streak += 1
        else:
            break
    return f"Reading streak: {streak} consecutive day(s), sir."


def current_book() -> str:
    data = _load()
    if not data["sessions"]:
        return "No reading sessions logged, sir."
    last = data["sessions"][-1]["book"]
    return f"You were last reading '{last}', sir."
