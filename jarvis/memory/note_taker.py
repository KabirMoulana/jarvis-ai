"""
jarvis/memory/note_taker.py
Persistent note-taking skill.
Notes are stored as a JSON file so they survive restarts.
Supports add, list, search, delete, and clear operations.
"""
import json
import os
from datetime import datetime

_NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.json")


def _load() -> list[dict]:
    if not os.path.exists(_NOTES_FILE):
        return []
    with open(_NOTES_FILE, "r") as f:
        return json.load(f)


def _save(notes: list[dict]):
    with open(_NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def add_note(text: str) -> str:
    """Save a new note and return confirmation."""
    notes = _load()
    note  = {
        "id":        len(notes) + 1,
        "text":      text.strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    notes.append(note)
    _save(notes)
    return f"Note #{note['id']} saved: "{text.strip()}""


def list_notes() -> str:
    """Return all notes as a formatted string."""
    notes = _load()
    if not notes:
        return "You have no saved notes."
    lines = [f"  #{n['id']} [{n['created_at']}] {n['text']}" for n in notes]
    return "Your notes:\n" + "\n".join(lines)


def search_notes(keyword: str) -> str:
    """Find notes containing the keyword."""
    notes   = _load()
    matches = [n for n in notes if keyword.lower() in n["text"].lower()]
    if not matches:
        return f"No notes found matching '{keyword}'."
    lines = [f"  #{n['id']} {n['text']}" for n in matches]
    return f"Found {len(matches)} note(s):\n" + "\n".join(lines)


def delete_note(note_id: int) -> str:
    """Delete a note by its ID."""
    notes    = _load()
    filtered = [n for n in notes if n["id"] != note_id]
    if len(filtered) == len(notes):
        return f"No note with ID {note_id}."
    _save(filtered)
    return f"Note #{note_id} deleted."


def clear_notes() -> str:
    """Delete all notes."""
    _save([])
    return "All notes cleared."
