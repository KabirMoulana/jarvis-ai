
"""Simple reminder command using threading timers."""
import threading
import re


def _remind(message: str) -> None:
    from utils.text_to_speech import speak
    speak(f"Reminder: {message}")


def set_reminder(message: str, seconds: int) -> str:
    t = threading.Timer(seconds, _remind, args=(message,))
    t.daemon = True
    t.start()
    minutes = seconds // 60
    return f"Reminder set for {minutes} minute{'s' if minutes != 1 else ''}: {message}"


def handle(command: str) -> str | None:
    if "remind me" not in command:
        return None
    # Pattern: "remind me in X minutes to <message>"
    match = re.search(r"remind me in (\d+) minute", command)
    minutes = int(match.group(1)) if match else 1
    msg_match = re.search(r"to (.+)$", command)
    message = msg_match.group(1).strip() if msg_match else "do something"
    return set_reminder(message, minutes * 60)
