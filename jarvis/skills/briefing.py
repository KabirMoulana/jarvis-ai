"""
jarvis/skills/briefing.py
Daily briefing skill — JARVIS morning/evening report.
Combines: time, date, weather, a motivational note, and system status.
"""
from datetime import datetime
from jarvis.skills.vitals   import get_vitals
from jarvis.skills.web_skills import get_weather


_MORNING_QUOTES = [
    "Another day, another opportunity to be exceptional.",
    "The arc reactor doesn't power itself. Let's get to work.",
    "Shall I prepare your schedule, sir?",
    "All systems are green. The day awaits.",
    "Ready when you are, sir.",
]

_EVENING_QUOTES = [
    "Another productive day in the books, sir.",
    "All tasks complete. Time to recharge.",
    "Systems remain stable. Rest well, sir.",
    "The suit is powered down. You should be too.",
]


def get_briefing(location: str = "") -> str:
    """Return a full JARVIS-style daily briefing."""
    now      = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    hour     = now.hour

    if 5 <= hour < 12:
        greeting = f"Good morning, sir. It is {time_str} on {date_str}."
        quote    = _pick_quote(_MORNING_QUOTES, hour)
    elif 12 <= hour < 17:
        greeting = f"Good afternoon, sir. It is {time_str} on {date_str}."
        quote    = _pick_quote(_MORNING_QUOTES, hour)
    else:
        greeting = f"Good evening, sir. It is {time_str} on {date_str}."
        quote    = _pick_quote(_EVENING_QUOTES, hour)

    weather = get_weather(location) if location else ""
    vitals  = get_vitals()

    parts = [greeting]
    if weather:
        parts.append(weather)
    parts.append(vitals)
    parts.append(quote)

    return " ".join(parts)


def _pick_quote(pool: list[str], seed: int) -> str:
    return pool[seed % len(pool)]
