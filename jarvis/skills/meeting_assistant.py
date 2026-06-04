"""
jarvis/skills/meeting_assistant.py
Meeting assistant — JARVIS helps prepare for and manage meetings.
Generates agendas, takes notes, and sends follow-ups.
"""
import json
import os
from datetime import datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "meetings.json")


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


def create_meeting(title: str, attendees: str = "", time: str = "", agenda: str = "") -> str:
    meetings = _load()
    meeting  = {
        "id":        len(meetings) + 1,
        "title":     title,
        "attendees": [a.strip() for a in attendees.split(",") if a.strip()],
        "time":      time or datetime.now().isoformat(),
        "agenda":    agenda,
        "notes":     [],
        "actions":   [],
    }
    meetings.append(meeting)
    _save(meetings)
    att = f" with {attendees}" if attendees else ""
    return f"Meeting '{title}'{att} created, sir."


def add_meeting_note(meeting_id: int, note: str) -> str:
    meetings = _load()
    for m in meetings:
        if m["id"] == meeting_id:
            m["notes"].append({"time": datetime.now().isoformat(), "note": note})
            _save(meetings)
            return f"Note added to meeting {meeting_id}, sir."
    return f"Meeting {meeting_id} not found, sir."


def add_action_item(meeting_id: int, action: str, owner: str = "") -> str:
    meetings = _load()
    for m in meetings:
        if m["id"] == meeting_id:
            m["actions"].append({"action": action, "owner": owner, "done": False})
            _save(meetings)
            return f"Action item added: {action}" + (f" — {owner}" if owner else "") + ", sir."
    return f"Meeting {meeting_id} not found, sir."


def get_meeting_summary(meeting_id: int) -> str:
    meetings = _load()
    for m in meetings:
        if m["id"] == meeting_id:
            notes   = len(m["notes"])
            actions = len(m["actions"])
            att     = ", ".join(m["attendees"]) if m["attendees"] else "no attendees"
            pending = [a for a in m["actions"] if not a["done"]]
            return (
                f"Meeting: {m['title']}. Attendees: {att}. "
                f"{notes} note(s), {actions} action item(s), "
                f"{len(pending)} pending, sir."
            )
    return f"Meeting {meeting_id} not found, sir."


def generate_agenda(topics: list[str], duration_mins: int = 60) -> str:
    """Generate a structured meeting agenda."""
    if not topics:
        return "No topics provided, sir."
    time_per = duration_mins // len(topics)
    agenda   = [f"Meeting Agenda — {duration_mins} minutes total"]
    for i, topic in enumerate(topics, 1):
        start = (i-1) * time_per
        agenda.append(f"{i}. {topic} ({time_per} min)")
    return " | ".join(agenda) + " | Q&A and wrap-up."


def list_meetings() -> str:
    meetings = _load()
    if not meetings:
        return "No meetings logged, sir."
    recent = meetings[-5:]
    parts  = [f"{m['id']}. {m['title']}" for m in reversed(recent)]
    return f"{len(meetings)} meeting(s) on record, sir. Recent: " + "; ".join(parts) + "."
