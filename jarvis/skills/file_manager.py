"""
jarvis/skills/file_manager.py
File management skill — JARVIS can find, list, open and organise files by voice.
Works within the user's home directory for safety.
"""
import os
import subprocess
import sys
import shutil
from datetime import datetime

_HOME = os.path.expanduser("~")
_SAFE_ROOTS = [_HOME]   # Only operate within home dir


def find_file(name: str, search_dir: str = _HOME) -> str:
    """Search for a file by name and return JARVIS-style result."""
    name    = name.strip()
    matches = []
    try:
        for root, dirs, files in os.walk(search_dir):
            # Skip hidden and system directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in
                       ("Library", "node_modules", "__pycache__", ".git")]
            for f in files:
                if name.lower() in f.lower():
                    matches.append(os.path.join(root, f))
            if len(matches) >= 10:
                break
    except PermissionError:
        pass

    if not matches:
        return f"No file matching '{name}' found in your home directory, sir."
    if len(matches) == 1:
        return f"Found it, sir: {matches[0]}"
    return f"Found {len(matches)} files matching '{name}', sir: " + "; ".join(matches[:5]) + "."


def list_directory(path: str = "") -> str:
    """List contents of a directory."""
    target = os.path.join(_HOME, path.strip()) if path else os.path.expanduser("~/Desktop")
    if not os.path.exists(target):
        return f"Directory not found: {target}, sir."
    try:
        items  = os.listdir(target)
        files  = [i for i in items if os.path.isfile(os.path.join(target, i)) and not i.startswith(".")]
        dirs   = [i for i in items if os.path.isdir(os.path.join(target, i))  and not i.startswith(".")]
        return (
            f"{os.path.basename(target)} contains {len(dirs)} folder(s) "
            f"and {len(files)} file(s), sir. "
            + (f"Files: {', '.join(files[:8])}." if files else "")
        )
    except Exception as e:
        return f"Could not list directory: {e}"


def open_file(path: str) -> str:
    """Open a file with the default application."""
    full_path = os.path.join(_HOME, path) if not os.path.isabs(path) else path
    if not os.path.exists(full_path):
        return f"File not found: {full_path}, sir."
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", full_path])
        elif sys.platform == "win32":
            os.startfile(full_path)
        else:
            subprocess.Popen(["xdg-open", full_path])
        return f"Opening {os.path.basename(full_path)}, sir."
    except Exception as e:
        return f"Could not open file: {e}"


def get_disk_usage(path: str = _HOME) -> str:
    """Return disk usage for a path."""
    try:
        usage = shutil.disk_usage(path)
        total = _fmt(usage.total)
        used  = _fmt(usage.used)
        free  = _fmt(usage.free)
        pct   = usage.used / usage.total * 100
        return f"Disk usage: {used} used of {total} total ({pct:.0f}%), {free} free, sir."
    except Exception as e:
        return f"Could not get disk usage: {e}"


def recent_downloads(count: int = 5) -> str:
    """List the most recently downloaded files."""
    dl_dir = os.path.expanduser("~/Downloads")
    if not os.path.exists(dl_dir):
        return "Downloads folder not found, sir."
    try:
        files = sorted(
            [f for f in os.listdir(dl_dir) if not f.startswith(".")],
            key=lambda f: os.path.getmtime(os.path.join(dl_dir, f)),
            reverse=True
        )[:count]
        if not files:
            return "Your Downloads folder is empty, sir."
        return f"Your {len(files)} most recent downloads: " + ", ".join(files) + "."
    except Exception as e:
        return f"Could not read Downloads: {e}"


def _fmt(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"
