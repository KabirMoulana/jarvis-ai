"""
jarvis/skills/clipboard.py
Clipboard skill — read, write, and transform clipboard contents.
Works on macOS, Windows, and Linux (xclip required on Linux).
"""
import subprocess
import sys


def read_clipboard() -> str:
    """Read and return current clipboard contents."""
    try:
        if sys.platform == "darwin":
            result = subprocess.run(["pbpaste"], capture_output=True, text=True)
            text   = result.stdout.strip()
        elif sys.platform == "win32":
            import tkinter as tk
            root = tk.Tk(); root.withdraw()
            text = root.clipboard_get(); root.destroy()
        else:
            result = subprocess.run(["xclip", "-selection", "clipboard", "-o"],
                                    capture_output=True, text=True)
            text   = result.stdout.strip()

        if not text:
            return "Clipboard is empty, sir."
        preview = text[:120] + "..." if len(text) > 120 else text
        return f"Clipboard contains: {preview}"
    except Exception as e:
        return f"Could not read clipboard: {e}"


def write_clipboard(text: str) -> str:
    """Write text to the clipboard."""
    try:
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif sys.platform == "win32":
            import tkinter as tk
            root = tk.Tk(); root.withdraw()
            root.clipboard_clear(); root.clipboard_append(text); root.update()
            root.destroy()
        else:
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=text.encode(), check=True)
        return "Text copied to clipboard, sir."
    except Exception as e:
        return f"Could not write to clipboard: {e}"


def clipboard_word_count() -> str:
    """Count words in the clipboard."""
    try:
        text  = _raw_clipboard()
        words = len(text.split())
        chars = len(text)
        return f"Clipboard contains {words} words and {chars} characters, sir."
    except Exception as e:
        return f"Could not analyse clipboard: {e}"


def clipboard_to_uppercase() -> str:
    text = _raw_clipboard()
    if not text:
        return "Clipboard is empty, sir."
    write_clipboard(text.upper())
    return "Clipboard text converted to uppercase, sir."


def _raw_clipboard() -> str:
    try:
        if sys.platform == "darwin":
            return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout
        return ""
    except Exception:
        return ""
