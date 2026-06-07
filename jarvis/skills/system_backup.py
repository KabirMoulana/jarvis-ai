"""
jarvis/skills/system_backup.py
System backup — JARVIS backs up important files and
JARVIS memory/config to a zip archive.
"""
import os
import zipfile
import shutil
from datetime import datetime

_JARVIS_MEMORY = os.path.join(os.path.dirname(__file__), "..", "memory")
_BACKUP_DIR    = os.path.expanduser("~/Desktop/JarvisBackups")


def backup_jarvis_memory() -> str:
    """Backup all JARVIS memory files to Desktop."""
    os.makedirs(_BACKUP_DIR, exist_ok=True)
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(_BACKUP_DIR, f"jarvis_memory_{timestamp}.zip")

    try:
        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
            memory_dir = os.path.abspath(_JARVIS_MEMORY)
            if os.path.exists(memory_dir):
                for root, dirs, files in os.walk(memory_dir):
                    for file in files:
                        filepath  = os.path.join(root, file)
                        arcname   = os.path.relpath(filepath, os.path.dirname(memory_dir))
                        zf.write(filepath, arcname)
        size = os.path.getsize(backup_path)
        return (
            f"JARVIS memory backed up to Desktop/JarvisBackups/ "
            f"({size/1024:.1f} KB), sir."
        )
    except Exception as e:
        return f"Backup failed: {e}"


def backup_folder(folder_path: str, name: str = "") -> str:
    """Backup any folder to a zip archive on Desktop."""
    folder = os.path.expanduser(folder_path)
    if not os.path.exists(folder):
        return f"Folder not found: {folder}, sir."

    os.makedirs(_BACKUP_DIR, exist_ok=True)
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    label       = name or os.path.basename(folder)
    backup_path = os.path.join(_BACKUP_DIR, f"{label}_{timestamp}.zip")

    try:
        shutil.make_archive(backup_path.replace(".zip", ""), "zip", folder)
        size = os.path.getsize(backup_path)
        return f"'{label}' backed up ({size/1024:.1f} KB), sir."
    except Exception as e:
        return f"Backup failed: {e}"


def list_backups() -> str:
    if not os.path.exists(_BACKUP_DIR):
        return "No backups found, sir."
    files = sorted(
        [f for f in os.listdir(_BACKUP_DIR) if f.endswith(".zip")],
        reverse=True
    )[:5]
    if not files:
        return "No backups found in JarvisBackups, sir."
    return f"{len(files)} recent backup(s): " + ", ".join(files) + ", sir."


def restore_latest_backup() -> str:
    if not os.path.exists(_BACKUP_DIR):
        return "No backups directory found, sir."
    zips = sorted(
        [f for f in os.listdir(_BACKUP_DIR) if f.startswith("jarvis_memory") and f.endswith(".zip")],
        reverse=True
    )
    if not zips:
        return "No JARVIS memory backups found, sir."
    latest      = os.path.join(_BACKUP_DIR, zips[0])
    memory_dir  = os.path.abspath(_JARVIS_MEMORY)
    try:
        with zipfile.ZipFile(latest, "r") as zf:
            zf.extractall(os.path.dirname(memory_dir))
        return f"Memory restored from {zips[0]}, sir."
    except Exception as e:
        return f"Restore failed: {e}"
