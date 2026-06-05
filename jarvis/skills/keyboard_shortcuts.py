"""
jarvis/skills/keyboard_shortcuts.py
Keyboard shortcuts reference — JARVIS tells you shortcuts
for any app by voice. Covers macOS, Windows, VSCode, Chrome, etc.
"""

_SHORTCUTS = {
    "macos": {
        "copy":            "Cmd+C",
        "paste":           "Cmd+V",
        "cut":             "Cmd+X",
        "undo":            "Cmd+Z",
        "redo":            "Cmd+Shift+Z",
        "save":            "Cmd+S",
        "select all":      "Cmd+A",
        "find":            "Cmd+F",
        "new tab":         "Cmd+T",
        "close tab":       "Cmd+W",
        "spotlight":       "Cmd+Space",
        "screenshot":      "Cmd+Shift+3",
        "screenshot area": "Cmd+Shift+4",
        "lock screen":     "Cmd+Ctrl+Q",
        "force quit":      "Cmd+Option+Esc",
        "switch app":      "Cmd+Tab",
        "hide window":     "Cmd+H",
        "minimize":        "Cmd+M",
    },
    "windows": {
        "copy":            "Ctrl+C",
        "paste":           "Ctrl+V",
        "cut":             "Ctrl+X",
        "undo":            "Ctrl+Z",
        "redo":            "Ctrl+Y",
        "save":            "Ctrl+S",
        "select all":      "Ctrl+A",
        "find":            "Ctrl+F",
        "new tab":         "Ctrl+T",
        "close tab":       "Ctrl+W",
        "search":          "Win+S",
        "screenshot":      "Win+Shift+S",
        "lock screen":     "Win+L",
        "task manager":    "Ctrl+Shift+Esc",
        "switch app":      "Alt+Tab",
        "virtual desktop": "Win+Ctrl+D",
    },
    "vscode": {
        "command palette": "Cmd+Shift+P",
        "open file":       "Cmd+P",
        "toggle terminal": "Ctrl+`",
        "comment":         "Cmd+/",
        "format":          "Shift+Option+F",
        "go to line":      "Ctrl+G",
        "rename":          "F2",
        "find all":        "Cmd+Shift+F",
        "split editor":    "Cmd+\\",
        "close editor":    "Cmd+W",
        "zen mode":        "Cmd+K Z",
    },
    "chrome": {
        "new tab":         "Cmd+T",
        "new incognito":   "Cmd+Shift+N",
        "address bar":     "Cmd+L",
        "dev tools":       "Cmd+Option+I",
        "bookmark":        "Cmd+D",
        "history":         "Cmd+Y",
        "downloads":       "Cmd+Shift+J",
        "zoom in":         "Cmd++",
        "zoom out":        "Cmd+-",
        "full screen":     "Cmd+Shift+F",
    },
}


def get_shortcut(action: str, app: str = "") -> str:
    """Get a keyboard shortcut for an action."""
    action = action.lower().strip()
    app    = app.lower().strip()

    if app:
        for key in _SHORTCUTS:
            if app in key or key in app:
                shortcuts = _SHORTCUTS[key]
                for act, shortcut in shortcuts.items():
                    if action in act or act in action:
                        return f"{act.title()} in {key}: {shortcut}, sir."
        return f"No shortcut found for '{action}' in {app}, sir."

    # Search all apps
    results = []
    for app_name, shortcuts in _SHORTCUTS.items():
        for act, shortcut in shortcuts.items():
            if action in act or act in action:
                results.append(f"{app_name}: {shortcut}")
    if results:
        return f"Shortcut for '{action}': " + " | ".join(results) + ", sir."
    return f"No shortcut found for '{action}', sir."


def list_app_shortcuts(app: str) -> str:
    """List all shortcuts for an app."""
    app = app.lower()
    for key, shortcuts in _SHORTCUTS.items():
        if app in key or key in app:
            parts = [f"{act}: {sc}" for act, sc in list(shortcuts.items())[:8]]
            return f"{key.title()} shortcuts: " + " | ".join(parts) + ", sir."
    apps = ", ".join(_SHORTCUTS.keys())
    return f"App not found, sir. Available: {apps}."
