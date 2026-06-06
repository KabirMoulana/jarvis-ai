"""
jarvis/skills/event_planner.py
Event planner — JARVIS helps plan events, parties,
and gatherings with checklists and timelines.
"""
import json
import os
from datetime import date, datetime, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "events.json")

_CHECKLISTS = {
    "birthday party": [
        "Set the date and venue", "Create guest list", "Send invitations",
        "Order/bake cake", "Plan decorations", "Arrange food and drinks",
        "Prepare entertainment/activities", "Buy gift wrap and cards",
        "Confirm headcount", "Day-of setup",
    ],
    "dinner party": [
        "Choose date and guest list", "Send invitations",
        "Plan menu", "Check dietary requirements",
        "Shop for ingredients", "Prepare mise en place",
        "Set the table", "Prepare drinks/cocktails",
        "Cook the meal", "Enjoy!",
    ],
    "wedding": [
        "Set date and budget", "Book venue", "Choose officiant",
        "Send save-the-dates", "Book caterer", "Choose wedding party",
        "Send formal invitations", "Book photographer/videographer",
        "Plan honeymoon", "Order flowers", "Final fittings",
        "Rehearsal dinner", "Wedding day!",
    ],
    "conference": [
        "Define objectives and audience", "Set date and venue",
        "Create agenda", "Invite speakers", "Open registration",
        "Arrange catering", "Set up AV equipment",
        "Prepare materials/badges", "Day-of coordination", "Follow-up emails",
    ],
}


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


def create_event(name: str, event_date: str, event_type: str = "general") -> str:
    data      = _load()
    checklist = _CHECKLISTS.get(event_type.lower(), [])
    entry     = {
        "id":         len(data) + 1,
        "name":       name,
        "date":       event_date,
        "type":       event_type,
        "checklist":  [{"task": t, "done": False} for t in checklist],
        "notes":      [],
        "created":    str(date.today()),
    }
    data.append(entry)
    _save(data)
    return (
        f"Event '{name}' created for {event_date}, sir. "
        f"Checklist has {len(checklist)} items."
    )


def get_checklist(event_id: int) -> str:
    data = _load()
    for e in data:
        if e["id"] == event_id:
            items    = e["checklist"]
            done     = sum(1 for i in items if i["done"])
            pending  = [i["task"] for i in items if not i["done"]][:5]
            pct      = int(done / len(items) * 100) if items else 0
            return (
                f"'{e['name']}' checklist: {done}/{len(items)} done ({pct}%). "
                f"Next up: " + "; ".join(pending) + ", sir."
            )
    return f"Event {event_id} not found, sir."


def complete_checklist_item(event_id: int, task_keyword: str) -> str:
    data = _load()
    for e in data:
        if e["id"] == event_id:
            for item in e["checklist"]:
                if task_keyword.lower() in item["task"].lower():
                    item["done"] = True
                    _save(data)
                    return f"'{item['task']}' marked done, sir."
            return f"Task containing '{task_keyword}' not found, sir."
    return f"Event {event_id} not found, sir."


def days_until_event(event_id: int) -> str:
    data = _load()
    for e in data:
        if e["id"] == event_id:
            try:
                target = datetime.strptime(e["date"], "%Y-%m-%d").date()
                days   = (target - date.today()).days
                if days < 0:  return f"'{e['name']}' was {abs(days)} days ago, sir."
                if days == 0: return f"'{e['name']}' is today, sir!"
                return f"'{e['name']}' is in {days} days, sir."
            except Exception:
                return f"Invalid date for event {event_id}, sir."
    return f"Event {event_id} not found, sir."


def list_events() -> str:
    data = _load()
    if not data:
        return "No events planned, sir."
    parts = [f"#{e['id']} {e['name']} ({e['date']})" for e in data[-5:]]
    return f"{len(data)} event(s): " + " | ".join(parts) + ", sir."
