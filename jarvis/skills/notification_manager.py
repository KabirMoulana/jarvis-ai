"""
jarvis/skills/notification_manager.py
Desktop notifications — JARVIS sends native OS notifications.
Works on macOS, Windows, and Linux.
"""
import subprocess
import sys
import threading
import time


def send_notification(title: str, message: str, sound: bool = True) -> str:
    """Send a native desktop notification."""
    if sys.platform == "darwin":
        return _macos_notification(title, message, sound)
    elif sys.platform == "win32":
        return _windows_notification(title, message)
    else:
        return _linux_notification(title, message)


def _macos_notification(title: str, message: str, sound: bool) -> str:
    try:
        sound_str = "with sound name \"Submarine\"" if sound else ""
        script = (
            f'display notification "{message}" with title "{title}" '
            f'subtitle "J.A.R.V.I.S" {sound_str}'
        )
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
        return f"Notification sent: '{title}', sir."
    except Exception as e:
        return f"Notification failed: {e}"


def _windows_notification(title: str, message: str) -> str:
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5, threaded=True)
        return f"Notification sent: '{title}', sir."
    except ImportError:
        try:
            subprocess.run(["msg", "*", f"{title}: {message}"], capture_output=True)
            return f"Notification sent, sir."
        except Exception:
            return "Windows notifications require: pip install win10toast"


def _linux_notification(title: str, message: str) -> str:
    try:
        subprocess.run(["notify-send", title, message], capture_output=True, timeout=5)
        return f"Notification sent: '{title}', sir."
    except FileNotFoundError:
        return "Linux notifications require: sudo apt install libnotify-bin"
    except Exception as e:
        return f"Notification failed: {e}"


def schedule_notification(title: str, message: str, delay_secs: int) -> str:
    """Schedule a notification after a delay."""
    def _fire():
        time.sleep(delay_secs)
        send_notification(title, message)

    t = threading.Thread(target=_fire, daemon=True)
    t.start()

    mins, secs = divmod(delay_secs, 60)
    time_str   = f"{mins}m {secs}s" if mins else f"{secs}s"
    return f"Notification scheduled for {time_str} from now, sir."


def test_notification() -> str:
    """Send a test notification."""
    return send_notification("J.A.R.V.I.S", "All systems operational, sir.")
