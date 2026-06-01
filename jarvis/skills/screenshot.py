"""
jarvis/skills/screenshot.py
Screenshot skill — captures the screen and saves with a timestamp.
Uses Pillow (PIL) for cross-platform capture.
Install: pip install Pillow
"""
import os
import datetime

_SAVE_DIR = os.path.expanduser("~/Desktop/jarvis_screenshots")


def take_screenshot(save_dir: str = _SAVE_DIR) -> str:
    """Capture the full screen and save to disk."""
    try:
        from PIL import ImageGrab
    except ImportError:
        return "Screenshot unavailable, sir. Run: pip install Pillow"

    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = os.path.join(save_dir, f"jarvis_{timestamp}.png")

    try:
        img = ImageGrab.grab()
        img.save(filename)
        return f"Screenshot saved to your Desktop as jarvis_{timestamp}.png, sir."
    except Exception as e:
        return f"Screenshot failed: {e}"


def take_region_screenshot(x: int, y: int, width: int, height: int) -> str:
    """Capture a specific region of the screen."""
    try:
        from PIL import ImageGrab
    except ImportError:
        return "Screenshot unavailable. Run: pip install Pillow"

    os.makedirs(_SAVE_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = os.path.join(_SAVE_DIR, f"jarvis_region_{timestamp}.png")

    try:
        img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        img.save(filename)
        return f"Region screenshot saved as jarvis_region_{timestamp}.png, sir."
    except Exception as e:
        return f"Region screenshot failed: {e}"


def list_screenshots() -> str:
    """List recent screenshots taken by JARVIS."""
    if not os.path.exists(_SAVE_DIR):
        return "No screenshots taken yet, sir."
    files = sorted(
        [f for f in os.listdir(_SAVE_DIR) if f.endswith(".png")],
        reverse=True
    )[:5]
    if not files:
        return "No screenshots found, sir."
    return f"Your {len(files)} most recent screenshots: " + ", ".join(files) + "."
