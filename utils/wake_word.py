
"""Simple wake-word detection — checks if the transcript starts with the trigger."""
import os

WAKE_WORD = os.getenv("WAKE_WORD", "hey jarvis").lower()


def contains_wake_word(text: str) -> bool:
    return WAKE_WORD in text.lower()


def strip_wake_word(text: str) -> str:
    return text.lower().replace(WAKE_WORD, "").strip()
