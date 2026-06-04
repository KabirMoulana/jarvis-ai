"""
jarvis/skills/typing_test.py
Typing speed test — JARVIS tests your WPM and accuracy.
Displays a passage, times your input, calculates WPM.
"""
import time
import random

_PASSAGES = [
    "The quick brown fox jumps over the lazy dog near the river bank.",
    "Technology is best when it brings people together and makes their lives easier.",
    "In the middle of difficulty lies opportunity and the seed of an equal benefit.",
    "The arc reactor doesn't power itself. Hard work and persistence are the fuel.",
    "Success is not final, failure is not fatal. It is the courage to continue that counts.",
    "Artificial intelligence is not a replacement for human intelligence but an amplification.",
    "Every great developer you know got there by solving problems they were unqualified to solve.",
]

_active_test: dict = {}


def start_typing_test() -> str:
    """Start a typing speed test."""
    global _active_test
    passage = random.choice(_PASSAGES)
    _active_test = {
        "passage":    passage,
        "start_time": time.time(),
        "active":     True,
    }
    return f"Typing test started, sir. Type the following: '{passage}'"


def submit_typing_result(typed: str) -> str:
    """Submit typed text and calculate WPM and accuracy."""
    global _active_test
    if not _active_test.get("active"):
        return "No active typing test, sir. Say 'start typing test' first."

    elapsed  = time.time() - _active_test["start_time"]
    passage  = _active_test["passage"]
    _active_test["active"] = False

    # WPM calculation
    word_count = len(typed.split())
    wpm        = int((word_count / elapsed) * 60)

    # Accuracy calculation
    original_words = passage.lower().split()
    typed_words    = typed.lower().split()
    correct        = sum(1 for o, t in zip(original_words, typed_words) if o == t)
    accuracy       = int(correct / len(original_words) * 100) if original_words else 0

    rating = "excellent" if wpm >= 80 else "good" if wpm >= 60 else "average" if wpm >= 40 else "needs practice"
    return (
        f"Typing test complete, sir. "
        f"Speed: {wpm} WPM ({rating}). "
        f"Accuracy: {accuracy}%. "
        f"Time: {elapsed:.1f} seconds."
    )


def get_wpm_benchmark() -> str:
    """Return WPM benchmarks for context."""
    return (
        "Typing benchmarks, sir: "
        "Below 30 WPM: beginner. "
        "30-60 WPM: average. "
        "60-80 WPM: good. "
        "80-100 WPM: fast. "
        "100+ WPM: professional typist."
    )
