"""
jarvis/skills/joke_of_day.py
Joke of the day — JARVIS delivers a fresh daily joke
with full setup/punchline timing for comedic effect.
Also logs laugh history (just kidding — it logs which jokes were told).
"""
import json
import os
import random
from datetime import date

_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "jokes_told.json")

_JOKES_DAILY = [
    ("Why did the AI go to therapy?", "It had too many deep learning issues, sir."),
    ("What do you call a JARVIS that tells bad jokes?", "A pun-intentional side effect, sir."),
    ("Why did Tony Stark install air conditioning in the lab?", "He heard the CPU was overheating, sir."),
    ("What's an AI's favourite type of music?", "Heavy metal... because of all the iron, sir."),
    ("Why don't programmers like nature?", "Too many bugs and no documentation, sir."),
    ("What did the quantum physicist say when he wanted to fight?", "Let me atom, sir."),
    ("Why can't you trust atoms?", "They make up literally everything, sir."),
    ("I asked the AI to tell me a joke about infinity.", "It's still going, sir."),
    ("What's a robot's favourite dance?", "The algorithm, sir."),
    ("Why did the developer go broke?", "He used up all his cache, sir."),
    ("What do you call two birds who are in love?", "Tweethearts, sir."),
    ("I tried to write a joke about time travel.", "You didn't laugh yet, but you will, sir."),
]


def get_joke_of_day() -> tuple[str, str]:
    """Return today's joke — consistent for the entire day."""
    idx = date.today().toordinal() % len(_JOKES_DAILY)
    _log_joke(idx)
    return _JOKES_DAILY[idx]


def get_joke_of_day_str() -> str:
    setup, punchline = get_joke_of_day()
    return f"{setup} ... {punchline}"


def get_random_daily_joke() -> str:
    setup, punchline = random.choice(_JOKES_DAILY)
    return f"{setup} {punchline}"


def _log_joke(idx: int):
    try:
        data = {}
        if os.path.exists(_LOG_FILE):
            with open(_LOG_FILE) as f:
                data = json.load(f)
        data[str(date.today())] = idx
        os.makedirs(os.path.dirname(_LOG_FILE), exist_ok=True)
        with open(_LOG_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def get_joke_streak() -> str:
    """How many days in a row has JARVIS told a joke?"""
    try:
        if not os.path.exists(_LOG_FILE):
            return "No joke history yet, sir."
        with open(_LOG_FILE) as f:
            data = json.load(f)
        dates  = sorted(data.keys(), reverse=True)
        streak = 1
        for i in range(1, len(dates)):
            from datetime import date, timedelta
            d1 = date.fromisoformat(dates[i-1])
            d2 = date.fromisoformat(dates[i])
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        return f"JARVIS has told a joke for {streak} consecutive day(s), sir."
    except Exception:
        return "Joke streak data unavailable, sir."
