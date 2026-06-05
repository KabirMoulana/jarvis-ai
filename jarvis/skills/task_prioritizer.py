"""
jarvis/skills/task_prioritizer.py
Task prioritizer — JARVIS ranks your tasks using the
Eisenhower Matrix (urgent/important) and MoSCoW method.
"""
import json
import os
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "priority_tasks.json")


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
        json.dump(data, f, indent=2)


def add_task(task: str, urgent: bool = False, important: bool = False) -> str:
    """Add a task with Eisenhower Matrix classification."""
    data  = _load()
    if urgent and important:
        quadrant = "Do First"
        advice   = "Do this immediately."
    elif important and not urgent:
        quadrant = "Schedule"
        advice   = "Plan time to do this properly."
    elif urgent and not important:
        quadrant = "Delegate"
        advice   = "Consider delegating this."
    else:
        quadrant = "Eliminate"
        advice   = "Question whether this is necessary."

    entry = {
        "id":        len(data) + 1,
        "task":      task,
        "urgent":    urgent,
        "important": important,
        "quadrant":  quadrant,
        "done":      False,
        "date":      str(date.today()),
    }
    data.append(entry)
    _save(data)
    return f"Task '{task}' added — {quadrant}. {advice}, sir."


def get_priority_list() -> str:
    """Return tasks sorted by Eisenhower quadrant."""
    data    = _load()
    pending = [t for t in data if not t["done"]]
    if not pending:
        return "No pending tasks, sir."
    order   = {"Do First": 1, "Schedule": 2, "Delegate": 3, "Eliminate": 4}
    sorted_tasks = sorted(pending, key=lambda t: order.get(t["quadrant"], 5))
    parts = []
    for t in sorted_tasks[:8]:
        parts.append(f"[{t['quadrant']}] {t['task']}")
    return "Priority list, sir: " + " | ".join(parts) + "."


def complete_task(task_id: int) -> str:
    data = _load()
    for t in data:
        if t["id"] == task_id:
            t["done"] = True
            _save(data)
            return f"Task {task_id} complete, sir."
    return f"Task {task_id} not found, sir."


def explain_matrix() -> str:
    return (
        "The Eisenhower Matrix, sir: "
        "Urgent + Important = Do First immediately. "
        "Important + Not Urgent = Schedule for later. "
        "Urgent + Not Important = Delegate to someone else. "
        "Not Urgent + Not Important = Eliminate or ignore."
    )
