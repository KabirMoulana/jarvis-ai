"""
jarvis/skills/system_commands.py
Advanced system commands — JARVIS controls system settings
by voice: brightness, dark mode, Do Not Disturb, WiFi toggle.
macOS focused with cross-platform notes.
"""
import subprocess
import sys
import os


def set_brightness(level: int) -> str:
    """Set screen brightness 0-100. macOS only."""
    level = max(0, min(100, level))
    if sys.platform == "darwin":
        try:
            val = level / 100.0
            subprocess.run(["osascript", "-e",
                f"tell application \"System Events\" to set brightness of (every desktop) to {val}"],
                capture_output=True)
            return f"Brightness set to {level}%, sir."
        except Exception as e:
            return f"Brightness control failed: {e}"
    return "Brightness control is macOS-only, sir."


def toggle_dark_mode() -> str:
    """Toggle macOS dark/light mode."""
    if sys.platform == "darwin":
        script = 'tell app "System Events" to tell appearance preferences to set dark mode to not dark mode'
        subprocess.run(["osascript", "-e", script], capture_output=True)
        return "Dark mode toggled, sir."
    return "Dark mode toggle is macOS-only, sir."


def enable_do_not_disturb() -> str:
    """Enable Do Not Disturb on macOS."""
    if sys.platform == "darwin":
        script = 'tell application "System Events" to set do not disturb to true'
        subprocess.run(["osascript", "-e", script], capture_output=True)
        return "Do Not Disturb enabled, sir. Focus mode activated."
    return "Do Not Disturb is macOS-only, sir."


def disable_do_not_disturb() -> str:
    if sys.platform == "darwin":
        script = 'tell application "System Events" to set do not disturb to false'
        subprocess.run(["osascript", "-e", script], capture_output=True)
        return "Do Not Disturb disabled, sir."
    return "Do Not Disturb is macOS-only, sir."


def lock_screen() -> str:
    """Lock the screen."""
    if sys.platform == "darwin":
        subprocess.run(["pmset", "displaysleepnow"])
        return "Screen locked, sir."
    elif sys.platform == "win32":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        return "Screen locked, sir."
    else:
        subprocess.run(["xdg-screensaver", "lock"])
        return "Screen locked, sir."


def empty_trash() -> str:
    """Empty the Trash / Recycle Bin."""
    if sys.platform == "darwin":
        subprocess.run(["osascript", "-e", 'tell application "Finder" to empty trash'],
                       capture_output=True)
        return "Trash emptied, sir."
    return "Trash emptying is macOS-only via this method, sir."


def get_wifi_name() -> str:
    """Get the current WiFi network name."""
    if sys.platform == "darwin":
        result = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
            capture_output=True, text=True
        )
        for line in result.stdout.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return f"Connected to {line.split(':')[-1].strip()}, sir."
    try:
        import subprocess
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True)
        ssid   = result.stdout.strip()
        return f"Connected to {ssid}, sir." if ssid else "WiFi name unavailable, sir."
    except Exception:
        return "WiFi info unavailable, sir."


def set_volume_level(level: int) -> str:
    """Set system volume 0-100."""
    level = max(0, min(100, level))
    if sys.platform == "darwin":
        subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        return f"Volume set to {level}%, sir."
    return f"Volume control via voice is macOS-optimised, sir."
