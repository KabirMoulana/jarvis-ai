
"""Simple note-taking command — save and read notes to a local file."""
import os
from datetime import datetime

NOTES_FILE = os.path.expanduser("~/.jarvis_notes.txt")


def save_note(text: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE, "a") as f:
        f.write(f"[{timestamp}] {text}\n")
    return "Note saved."


def read_notes() -> str:
    if not os.path.exists(NOTES_FILE):
        return "You have no saved notes."
    with open(NOTES_FILE) as f:
        lines = f.read().strip()
    return lines or "Your notes are empty."


def handle(command: str) -> str | None:
    if "take a note" in command or "remember that" in command:
        note = command.replace("take a note", "").replace("remember that", "").strip()
        return save_note(note)
    if "read notes" in command or "show notes" in command:
        return read_notes()
    return None
