"""
jarvis/skills/todo.py
Task management — JARVIS-style to-do list with priorities.
Supports add, complete, delete, list, and priority filtering.
Persists to JSON.
"""
import json
import os
from datetime import datetime

_TODO_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "todos.json")
_todos: list[dict] = []


def _load():
    global _todos
    try:
        if os.path.exists(_TODO_FILE):
            with open(_TODO_FILE) as f:
                _todos = json.load(f)
    except Exception:
        _todos = []


def _save():
    os.makedirs(os.path.dirname(_TODO_FILE), exist_ok=True)
    with open(_TODO_FILE, "w") as f:
        json.dump(_todos, f, indent=2, default=str)


def add_task(task: str, priority: str = "normal") -> str:
    _load()
    priority = priority.lower().strip()
    if priority not in ("high", "normal", "low"):
        priority = "normal"
    entry = {
        "id":        len(_todos) + 1,
        "task":      task.strip(),
        "priority":  priority,
        "done":      False,
        "created":   datetime.now().isoformat(),
        "completed": None,
    }
    _todos.append(entry)
    _save()
    tag = f" [{priority.upper()} priority]" if priority != "normal" else ""
    return f"Task added{tag}: {task}, sir."


def complete_task(task_id: int) -> str:
    _load()
    for t in _todos:
        if t["id"] == task_id and not t["done"]:
            t["done"]      = True
            t["completed"] = datetime.now().isoformat()
            _save()
            return f"Task {task_id} marked complete, sir. Well done."
    return f"Task {task_id} not found or already completed, sir."


def delete_task(task_id: int) -> str:
    global _todos
    _load()
    before = len(_todos)
    _todos = [t for t in _todos if t["id"] != task_id]
    _save()
    if len(_todos) < before:
        return f"Task {task_id} removed, sir."
    return f"Task {task_id} not found, sir."


def list_tasks(show_done: bool = False, priority: str = "") -> str:
    _load()
    tasks = [t for t in _todos if show_done or not t["done"]]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority.lower()]
    if not tasks:
        return "No tasks found, sir." if priority else "Your to-do list is clear, sir."

    high   = [t for t in tasks if t["priority"] == "high"   and not t["done"]]
    normal = [t for t in tasks if t["priority"] == "normal" and not t["done"]]
    low    = [t for t in tasks if t["priority"] == "low"    and not t["done"]]
    done   = [t for t in tasks if t["done"]]

    parts = []
    if high:
        parts.append(f"High priority: " + "; ".join(f"{t['id']}. {t['task']}" for t in high))
    if normal:
        parts.append(f"Normal: " + "; ".join(f"{t['id']}. {t['task']}" for t in normal))
    if low:
        parts.append(f"Low priority: " + "; ".join(f"{t['id']}. {t['task']}" for t in low))
    if done and show_done:
        parts.append(f"Completed: {len(done)} task(s)")

    total = len([t for t in tasks if not t["done"]])
    return f"You have {total} pending task(s), sir. " + ". ".join(parts) + "."


def clear_completed() -> str:
    global _todos
    _load()
    before = len(_todos)
    _todos = [t for t in _todos if not t["done"]]
    _save()
    removed = before - len(_todos)
    return f"Cleared {removed} completed task(s), sir."


_load()
