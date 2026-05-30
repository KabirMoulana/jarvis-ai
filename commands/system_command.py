
"""Handles system-level commands like shutdown, sleep, open apps."""
import sys
import os
import subprocess


def handle(command: str) -> str | None:
    if "shutdown" in command or "turn off" in command:
        speak_then_exec("Shutting down the system.", _shutdown)
        return "Shutting down."
    if "sleep" in command or "hibernate" in command:
        return _sleep()
    if "open" in command:
        parts = command.replace("open", "").strip()
        return _open_app(parts)
    return None


def _shutdown():
    if sys.platform == "win32":
        os.system("shutdown /s /t 5")
    elif sys.platform == "darwin":
        os.system("osascript -e 'tell app "Finder" to shut down'")
    else:
        os.system("shutdown -h now")


def _sleep():
    if sys.platform == "darwin":
        os.system("pmset sleepnow")
        return "Going to sleep."
    return "Sleep is only supported on macOS for now."


def _open_app(app_name: str) -> str:
    if sys.platform == "darwin":
        os.system(f"open -a '{app_name}'")
    elif sys.platform == "win32":
        os.system(f"start {app_name}")
    else:
        subprocess.Popen([app_name])
    return f"Opening {app_name}."


def speak_then_exec(msg, fn):
    print("Jarvis:", msg)
    fn()
