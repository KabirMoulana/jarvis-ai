"""
jarvis/skills/system_skills.py
OS-level capabilities: app launcher, volume control,
system info, screenshot, clipboard read/write.
"""
import os
import sys
import platform
import subprocess
import shutil
import datetime


def get_system_info() -> str:
    """Return a one-line system summary."""
    uname = platform.uname()
    return (
        f"OS: {uname.system} {uname.release} | "
        f"Machine: {uname.machine} | "
        f"CPU: {uname.processor or 'unknown'}"
    )


def open_application(app_name: str) -> str:
    """Open an application by name (cross-platform best-effort)."""
    system = sys.platform
    try:
        if system == "darwin":
            subprocess.Popen(["open", "-a", app_name])
            return f"Opening {app_name}..."
        elif system.startswith("win"):
            subprocess.Popen(["start", app_name], shell=True)
            return f"Opening {app_name}..."
        else:
            # Linux — try the name as a command
            if shutil.which(app_name.lower()):
                subprocess.Popen([app_name.lower()])
                return f"Launching {app_name}..."
            return f"Could not find {app_name} on this system."
    except Exception as e:
        return f"Failed to open {app_name}: {e}"


def set_volume(level: str) -> str:
    """
    Set system volume.
    level can be: 'up', 'down', 'mute', or a number 0-100.
    macOS only for now.
    """
    if sys.platform != "darwin":
        return "Volume control is only supported on macOS right now."

    if level == "mute":
        subprocess.run(["osascript", "-e", "set volume output muted true"])
        return "Volume muted."
    if level == "up":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
        return "Volume up."
    if level == "down":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
        return "Volume down."
    try:
        val = max(0, min(100, int(level)))
        subprocess.run(["osascript", "-e", f"set volume output volume {val}"])
        return f"Volume set to {val}%."
    except ValueError:
        return f"Unknown volume level: {level}"


def take_screenshot(save_dir: str = ".") -> str:
    """Take a screenshot and save to save_dir (macOS/Linux)."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath  = os.path.join(save_dir, f"screenshot_{timestamp}.png")
    if sys.platform == "darwin":
        subprocess.run(["screencapture", "-x", filepath])
        return f"Screenshot saved to {filepath}"
    elif shutil.which("scrot"):
        subprocess.run(["scrot", filepath])
        return f"Screenshot saved to {filepath}"
    return "Screenshot not supported on this platform."


def read_clipboard() -> str:
    """Read text from system clipboard."""
    if sys.platform == "darwin":
        result = subprocess.run(["pbpaste"], capture_output=True, text=True)
        return result.stdout.strip() or "(clipboard is empty)"
    return "Clipboard reading not supported on this platform."


def write_clipboard(text: str) -> str:
    """Write text to system clipboard."""
    if sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=text.encode())
        return "Copied to clipboard."
    return "Clipboard writing not supported on this platform."
