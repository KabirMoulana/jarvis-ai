"""
jarvis/hud.py
Terminal HUD — live status display for JARVIS.
Shows what Jarvis is currently doing in a clean status bar.
Inspired by Iron Man's heads-up display.
"""
import sys
import time
import threading
import shutil


_STATES = {
    "idle":       "◉  Standing by ...",
    "listening":  "🎙  Listening ...",
    "thinking":   "⚙   Processing ...",
    "speaking":   "🔊  Speaking ...",
    "booting":    "⚡  Initialising ...",
    "timer":      "⏱  Timer active ...",
    "searching":  "🔍  Searching ...",
    "error":      "⚠   Error detected",
}

_current_state  = "idle"
_spinner_chars  = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
_spinner_idx    = 0
_running        = False
_lock           = threading.Lock()
_thread         = None


def set_state(state: str, detail: str = ""):
    global _current_state
    with _lock:
        _current_state = state
    _render(detail)


def _render(detail: str = ""):
    global _spinner_idx
    term_width = shutil.get_terminal_size((80, 20)).columns
    label      = _STATES.get(_current_state, _current_state)
    spinner    = _spinner_chars[_spinner_idx % len(_spinner_chars)]
    _spinner_idx += 1

    line = f"\r  {spinner}  JARVIS  │  {label}"
    if detail:
        line += f"  │  {detail}"
    line = line[:term_width - 2].ljust(term_width - 2)
    sys.stdout.write(line)
    sys.stdout.flush()


def start():
    """Start the live HUD spinner in a background thread."""
    global _running, _thread
    _running = True

    def _loop():
        while _running:
            with _lock:
                pass
            _render()
            time.sleep(0.1)

    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()


def stop():
    global _running
    _running = False
    sys.stdout.write("\r" + " " * shutil.get_terminal_size((80, 20)).columns + "\r")
    sys.stdout.flush()


def print_above(text: str):
    """Print a line above the HUD without disrupting it."""
    sys.stdout.write(f"\r{' ' * shutil.get_terminal_size((80,20)).columns}\r")
    print(text)
