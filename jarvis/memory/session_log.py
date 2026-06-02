"""
jarvis/memory/session_log.py
Session logger — records every interaction JARVIS has.
Logs are saved as daily JSON files for review and analytics.
"""
import json
import os
from datetime import datetime, date

_LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")


def _log_path() -> str:
    os.makedirs(_LOG_DIR, exist_ok=True)
    return os.path.join(_LOG_DIR, f"session_{date.today()}.json")


def _load_today() -> list[dict]:
    path = _log_path()
    try:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def log_interaction(user_input: str, jarvis_response: str, intent: str = ""):
    """Log a single user↔JARVIS interaction."""
    logs = _load_today()
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "intent":    intent,
        "user":      user_input,
        "jarvis":    jarvis_response,
    })
    try:
        with open(_log_path(), "w") as f:
            json.dump(logs, f, indent=2, default=str)
    except Exception:
        pass


def get_session_stats() -> str:
    """Return stats about today's session."""
    logs = _load_today()
    if not logs:
        return "No interactions logged today, sir."

    intents = {}
    for entry in logs:
        intent = entry.get("intent", "unknown")
        intents[intent] = intents.get(intent, 0) + 1

    top_intent = max(intents, key=intents.get) if intents else "none"
    first_time = logs[0]["timestamp"][:16].replace("T", " ") if logs else "N/A"

    return (
        f"Session stats for today, sir. "
        f"{len(logs)} interactions logged since {first_time}. "
        f"Most used: '{top_intent}' ({intents.get(top_intent, 0)} times)."
    )


def get_recent_interactions(count: int = 5) -> str:
    """Return the last N interactions as a spoken summary."""
    logs = _load_today()
    if not logs:
        return "No interactions logged today, sir."
    recent = logs[-count:]
    parts  = [f"{e['user']} → {e['jarvis'][:60]}" for e in recent]
    return f"Last {len(recent)} interactions: " + ". ".join(parts) + "."


def clear_today_logs() -> str:
    """Clear today's session log."""
    path = _log_path()
    try:
        if os.path.exists(path):
            os.remove(path)
        return "Today's session log cleared, sir."
    except Exception as e:
        return f"Could not clear logs: {e}"
