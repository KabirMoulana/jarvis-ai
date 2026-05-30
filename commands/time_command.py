
"""Handles time and date related commands."""
from datetime import datetime


def get_time() -> str:
    return f"The current time is {datetime.now().strftime('%I:%M %p')}."


def get_date() -> str:
    return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."


def handle(command: str) -> str | None:
    if "time" in command:
        return get_time()
    if "date" in command or "today" in command:
        return get_date()
    return None
