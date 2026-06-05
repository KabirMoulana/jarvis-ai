"""
jarvis/skills/voice_notes_ai.py
AI-powered voice notes — JARVIS takes voice notes, auto-tags them,
and generates action items using the LLM.
"""
import json
import os
from datetime import datetime, date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "ai_notes.json")


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(data: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def _auto_tag(text: str) -> list[str]:
    tags     = []
    text_low = text.lower()
    if any(w in text_low for w in ["meet", "call", "zoom", "team"]):
        tags.append("meeting")
    if any(w in text_low for w in ["todo", "to do", "task", "reminder", "do this"]):
        tags.append("action")
    if any(w in text_low for w in ["idea", "think", "what if", "maybe", "could"]):
        tags.append("idea")
    if any(w in text_low for w in ["buy", "order", "purchase", "get"]):
        tags.append("shopping")
    if any(w in text_low for w in ["call", "email", "message", "contact"]):
        tags.append("communication")
    return tags or ["general"]


def save_note(text: str, llm_client=None) -> str:
    """Save a note with auto-tagging and optional AI summary."""
    notes = _load()
    tags  = _auto_tag(text)

    summary = ""
    if llm_client and llm_client.is_available():
        try:
            summary = llm_client.chat(
                f"Summarise this note in one sentence and extract any action items: {text}"
            )
        except Exception:
            pass

    entry = {
        "id":      len(notes) + 1,
        "text":    text.strip(),
        "tags":    tags,
        "summary": summary,
        "date":    datetime.now().isoformat(),
    }
    notes.append(entry)
    _save(notes)
    tag_str = ", ".join(tags)
    return f"Note #{entry['id']} saved and tagged as [{tag_str}], sir."


def search_notes(query: str) -> str:
    notes   = _load()
    matches = [n for n in notes if query.lower() in n["text"].lower()
               or query.lower() in " ".join(n["tags"])]
    if not matches:
        return f"No notes matching '{query}', sir."
    parts = [f"#{n['id']} [{', '.join(n['tags'])}]: {n['text'][:60]}" for n in matches[-3:]]
    return f"Found {len(matches)} note(s): " + " | ".join(parts) + ", sir."


def get_notes_by_tag(tag: str) -> str:
    notes   = _load()
    matches = [n for n in notes if tag.lower() in [t.lower() for t in n["tags"]]]
    if not matches:
        return f"No notes tagged '{tag}', sir."
    parts = [f"#{n['id']}: {n['text'][:60]}" for n in matches[-5:]]
    return f"{len(matches)} '{tag}' note(s): " + " | ".join(parts) + ", sir."


def get_action_items() -> str:
    notes   = _load()
    actions = [n for n in notes if "action" in n["tags"]]
    if not actions:
        return "No action items in your notes, sir."
    parts = [f"#{n['id']}: {n['text'][:60]}" for n in actions[-5:]]
    return f"{len(actions)} action item(s): " + " | ".join(parts) + ", sir."


def get_today_notes() -> str:
    notes = _load()
    today = str(date.today())
    todays = [n for n in notes if n["date"].startswith(today)]
    if not todays:
        return "No notes from today, sir."
    return f"{len(todays)} note(s) today: " + " | ".join(
        f"#{n['id']}: {n['text'][:50]}" for n in todays
    ) + ", sir."
