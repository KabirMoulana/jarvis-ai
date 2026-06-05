"""
jarvis/skills/clipboard_history.py
Clipboard history — JARVIS remembers the last 20 things copied.
Retrieve any previous clipboard entry by index or search.
"""
import json
import os
import subprocess
import sys
from datetime import datetime

_FILE    = os.path.join(os.path.dirname(__file__), "..", "memory", "clipboard_history.json")
_MAX     = 20
_history = []


def _load():
    global _history
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                _history = json.load(f)
    except Exception:
        _history = []


def _save():
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(_history, f, indent=2)


def _get_clipboard() -> str:
    try:
        if sys.platform == "darwin":
            return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout
    except Exception:
        pass
    return ""


def _set_clipboard(text: str):
    try:
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
    except Exception:
        pass


def capture_clipboard() -> str:
    """Capture and store the current clipboard content."""
    _load()
    text = _get_clipboard().strip()
    if not text:
        return "Clipboard is empty, sir."
    if _history and _history[-1]["text"] == text:
        return "Clipboard unchanged since last capture, sir."
    entry = {
        "id":      len(_history) + 1,
        "text":    text[:200],
        "time":    datetime.now().isoformat(),
        "preview": text[:40] + "..." if len(text) > 40 else text,
    }
    _history.append(entry)
    if len(_history) > _MAX:
        _history.pop(0)
    _save()
    return f"Clipboard entry {entry['id']} captured: '{entry['preview']}', sir."


def get_history(count: int = 5) -> str:
    _load()
    if not _history:
        return "No clipboard history yet, sir."
    recent = _history[-count:]
    parts  = [f"{e['id']}. {e['preview']}" for e in reversed(recent)]
    return f"Clipboard history ({len(_history)} entries): " + " | ".join(parts) + ", sir."


def restore_entry(entry_id: int) -> str:
    _load()
    for e in _history:
        if e["id"] == entry_id:
            _set_clipboard(e["text"])
            return f"Restored clipboard entry {entry_id}: '{e['preview']}', sir."
    return f"Entry {entry_id} not found, sir."


def search_history(query: str) -> str:
    _load()
    matches = [e for e in _history if query.lower() in e["text"].lower()]
    if not matches:
        return f"No clipboard history contains '{query}', sir."
    parts = [f"{e['id']}. {e['preview']}" for e in matches[-3:]]
    return f"Found {len(matches)} match(es): " + " | ".join(parts) + ", sir."


def clear_history() -> str:
    global _history
    _history = []
    _save()
    return "Clipboard history cleared, sir."
