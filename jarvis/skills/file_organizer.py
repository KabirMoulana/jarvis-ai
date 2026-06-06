"""
jarvis/skills/file_organizer.py
File organizer — JARVIS organises your Downloads folder
by automatically sorting files into categorised subfolders.
"""
import os
import shutil
from datetime import date

_CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff"],
    "Videos":     [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
    "Spreadsheets":[".xls", ".xlsx", ".csv", ".numbers"],
    "Slides":     [".ppt", ".pptx", ".key"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
    "Executables":[".exe", ".dmg", ".pkg", ".deb", ".app"],
    "Data":       [".json", ".xml", ".yaml", ".yml", ".sql", ".db"],
}


def organise_downloads(dry_run: bool = False) -> str:
    """Sort files in ~/Downloads into category folders."""
    dl_dir = os.path.expanduser("~/Downloads")
    if not os.path.exists(dl_dir):
        return "Downloads folder not found, sir."

    files   = [f for f in os.listdir(dl_dir)
               if os.path.isfile(os.path.join(dl_dir, f)) and not f.startswith(".")]
    if not files:
        return "Downloads folder is already empty, sir."

    moved  = {}
    skipped = []

    for filename in files:
        ext     = os.path.splitext(filename)[1].lower()
        dest_cat = "Other"
        for cat, exts in _CATEGORIES.items():
            if ext in exts:
                dest_cat = cat
                break

        src     = os.path.join(dl_dir, filename)
        dest_dir = os.path.join(dl_dir, dest_cat)

        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
            try:
                shutil.move(src, os.path.join(dest_dir, filename))
                moved[dest_cat] = moved.get(dest_cat, 0) + 1
            except Exception:
                skipped.append(filename)
        else:
            moved[dest_cat] = moved.get(dest_cat, 0) + 1

    mode  = "Would move" if dry_run else "Moved"
    parts = [f"{v} to {k}" for k, v in sorted(moved.items())]
    total = sum(moved.values())
    return (
        f"{mode} {total} file(s), sir: " + ", ".join(parts) + "."
        + (f" Skipped: {len(skipped)}." if skipped else "")
    )


def organise_folder(folder_path: str) -> str:
    """Organise a specific folder."""
    path = os.path.expanduser(folder_path)
    if not os.path.exists(path):
        return f"Folder not found: {path}, sir."
    original_dl = os.path.expanduser("~/Downloads")
    # Temporarily target the given folder
    files   = [f for f in os.listdir(path)
               if os.path.isfile(os.path.join(path, f)) and not f.startswith(".")]
    moved   = 0
    for filename in files:
        ext     = os.path.splitext(filename)[1].lower()
        dest_cat = "Other"
        for cat, exts in _CATEGORIES.items():
            if ext in exts:
                dest_cat = cat
                break
        dest_dir = os.path.join(path, dest_cat)
        os.makedirs(dest_dir, exist_ok=True)
        try:
            shutil.move(os.path.join(path, filename), os.path.join(dest_dir, filename))
            moved += 1
        except Exception:
            pass
    return f"Organised {moved} file(s) in {os.path.basename(path)}, sir."


def preview_organisation() -> str:
    """Preview what would be moved without actually moving."""
    return organise_downloads(dry_run=True)
