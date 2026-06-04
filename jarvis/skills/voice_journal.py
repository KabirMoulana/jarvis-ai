"""
jarvis/skills/voice_journal.py
Voice journal — JARVIS records your daily thoughts and reflections.
Entries saved as JSON with timestamps, searchable, and exportable.
"""
import json
import os
from datetime import datetime, date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "journal.json")


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(entries: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(entries, f, indent=2, default=str)


def add_entry(text: str, mood: str = "") -> str:
    """Add a journal entry."""
    entries = _load()
    entry   = {
        "id":        len(entries) + 1,
        "date":      datetime.now().isoformat(),
        "text":      text.strip(),
        "mood":      mood.lower().strip() if mood else "",
        "word_count": len(text.split()),
    }
    entries.append(entry)
    _save(entries)
    return (
        f"Journal entry #{entry['id']} saved, sir. "
        f"{entry['word_count']} words recorded at "
        f"{datetime.now().strftime('%I:%M %p')}."
    )


def get_today_entries() -> str:
    """Return all journal entries from today."""
    entries = _load()
    today   = str(date.today())
    todays  = [e for e in entries if e["date"].startswith(today)]
    if not todays:
        return "No journal entries for today yet, sir."
    parts = [f"Entry {e['id']}: {e['text'][:100]}" for e in todays]
    return f"Today's journal — {len(todays)} entries: " + ". ".join(parts) + "."


def search_journal(keyword: str) -> str:
    """Search journal entries for a keyword."""
    entries = _load()
    matches = [e for e in entries if keyword.lower() in e["text"].lower()]
    if not matches:
        return f"No journal entries containing '{keyword}', sir."
    results = [f"{e['date'][:10]}: {e['text'][:80]}" for e in matches[-3:]]
    return f"Found {len(matches)} entries mentioning '{keyword}', sir. Recent: " + ". ".join(results) + "."


def get_journal_stats() -> str:
    """Return statistics about the journal."""
    entries = _load()
    if not entries:
        return "No journal entries yet, sir."
    total_words = sum(e.get("word_count", 0) for e in entries)
    days        = len(set(e["date"][:10] for e in entries))
    moods       = [e["mood"] for e in entries if e.get("mood")]
    mood_str    = f" Most common mood: {max(set(moods), key=moods.count)}." if moods else ""
    return (
        f"Journal stats, sir: {len(entries)} entries across {days} days. "
        f"Total words: {total_words:,}.{mood_str}"
    )


def export_journal(path: str = "") -> str:
    """Export journal to a text file."""
    entries = _load()
    if not entries:
        return "No entries to export, sir."
    path = path or os.path.expanduser(f"~/Desktop/jarvis_journal_{date.today()}.txt")
    try:
        with open(path, "w") as f:
            for e in entries:
                f.write(f"[{e['date'][:16]}] {e['text']}\n\n")
        return f"Journal exported to {path}, sir."
    except Exception as ex:
        return f"Export failed: {ex}"
