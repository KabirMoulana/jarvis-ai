"""
jarvis/skills/voice_shortcuts.py
Custom voice shortcuts — users can define their own commands.
"When I say X, do Y" — stored in JSON, loaded on boot.
"""
import json
import os
import re

_SHORTCUTS_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "shortcuts.json")
_shortcuts: dict[str, str] = {}


def _load():
    global _shortcuts
    try:
        if os.path.exists(_SHORTCUTS_FILE):
            with open(_SHORTCUTS_FILE) as f:
                _shortcuts = json.load(f)
    except Exception:
        _shortcuts = {}


def _save():
    os.makedirs(os.path.dirname(_SHORTCUTS_FILE), exist_ok=True)
    with open(_SHORTCUTS_FILE, "w") as f:
        json.dump(_shortcuts, f, indent=2)


def add_shortcut(trigger: str, action: str) -> str:
    """Add a custom voice shortcut."""
    _load()
    trigger = trigger.lower().strip()
    _shortcuts[trigger] = action.strip()
    _save()
    return f"Shortcut saved, sir. When you say '{trigger}', I'll execute: {action}."


def remove_shortcut(trigger: str) -> str:
    _load()
    trigger = trigger.lower().strip()
    if trigger in _shortcuts:
        del _shortcuts[trigger]
        _save()
        return f"Shortcut '{trigger}' removed, sir."
    return f"No shortcut found for '{trigger}', sir."


def list_shortcuts() -> str:
    _load()
    if not _shortcuts:
        return "No custom shortcuts defined yet, sir. Say 'when I say X do Y' to create one."
    lines = [f"'{k}' → {v}" for k, v in _shortcuts.items()]
    return f"You have {len(_shortcuts)} custom shortcut(s): " + "; ".join(lines) + "."


def match_shortcut(text: str) -> str | None:
    """Check if input matches a custom shortcut. Returns the action or None."""
    _load()
    text_lower = text.lower().strip()
    for trigger, action in _shortcuts.items():
        if trigger in text_lower or text_lower == trigger:
            return action
    return None


def parse_shortcut_definition(text: str) -> tuple[str, str] | None:
    """
    Parse 'when I say good night run shutdown' or
    'add shortcut morning routine to start briefing'.
    Returns (trigger, action) or None.
    """
    patterns = [
        r"when(?:ever)? i say ['\"]?(.+?)['\"]?,? (?:then )?(?:do |run |execute )?(.+)",
        r"add shortcut ['\"]?(.+?)['\"]? to (.+)",
        r"shortcut ['\"]?(.+?)['\"]? (?:means?|does?|runs?) (.+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1).strip(), m.group(2).strip()
    return None


_load()
