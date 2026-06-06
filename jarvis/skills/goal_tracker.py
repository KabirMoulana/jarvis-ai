"""
jarvis/skills/goal_tracker.py
Goal tracker — JARVIS helps set, track, and achieve
short-term and long-term goals with milestones.
"""
import json
import os
from datetime import date, datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "goals.json")


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


def add_goal(title: str, description: str = "",
             target_date: str = "", category: str = "personal") -> str:
    data  = _load()
    entry = {
        "id":          len(data) + 1,
        "title":       title.strip(),
        "description": description.strip(),
        "category":    category.lower(),
        "target_date": target_date,
        "created":     str(date.today()),
        "progress":    0,
        "milestones":  [],
        "completed":   False,
    }
    data.append(entry)
    _save(data)
    date_str = f" by {target_date}" if target_date else ""
    return f"Goal '{title}' added{date_str}, sir."


def update_progress(goal_id: int, progress: int) -> str:
    data     = _load()
    progress = max(0, min(100, progress))
    for g in data:
        if g["id"] == goal_id:
            g["progress"] = progress
            if progress >= 100:
                g["completed"] = True
            _save(data)
            bar   = "█" * (progress // 10) + "░" * (10 - progress // 10)
            status = "COMPLETE!" if progress >= 100 else f"{progress}%"
            return f"Goal '{g['title']}' progress: [{bar}] {status}, sir."
    return f"Goal {goal_id} not found, sir."


def add_milestone(goal_id: int, milestone: str) -> str:
    data = _load()
    for g in data:
        if g["id"] == goal_id:
            g["milestones"].append({"text": milestone, "done": False})
            _save(data)
            return f"Milestone added to '{g['title']}', sir."
    return f"Goal {goal_id} not found, sir."


def list_goals(category: str = "") -> str:
    data = _load()
    if category:
        data = [g for g in data if category.lower() in g["category"]]
    active = [g for g in data if not g["completed"]]
    done   = [g for g in data if g["completed"]]
    if not data:
        return "No goals set, sir. Say 'add goal [title]' to start."
    parts = [f"#{g['id']} {g['title']} ({g['progress']}%)" for g in active[:5]]
    result = f"{len(active)} active goal(s): " + " | ".join(parts)
    if done:
        result += f" | {len(done)} completed."
    return result + ", sir."


def get_goal_summary() -> str:
    data      = _load()
    total     = len(data)
    completed = sum(1 for g in data if g["completed"])
    avg_prog  = sum(g["progress"] for g in data) / total if total else 0
    return (
        f"Goal summary, sir: {total} total, "
        f"{completed} completed, "
        f"{avg_prog:.0f}% average progress."
    )
