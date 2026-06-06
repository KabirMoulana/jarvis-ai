"""
jarvis/skills/hotkey_launcher.py
Hotkey launcher — JARVIS listens for global hotkeys
to trigger common actions without saying "Hey Jarvis".
Uses pynput for cross-platform hotkey detection.
"""
import threading
import os


_hotkeys     = {}
_listener    = None
_running     = False


def register_hotkey(combo: str, action_name: str, callback=None) -> str:
    """
    Register a global hotkey combination.
    combo format: 'ctrl+shift+j' or 'cmd+space'
    """
    _hotkeys[combo.lower()] = {"action": action_name, "callback": callback}
    return f"Hotkey '{combo}' registered for '{action_name}', sir."


def start_hotkey_listener(callback=None) -> str:
    """Start listening for registered hotkeys."""
    global _running, _listener
    if _running:
        return "Hotkey listener already active, sir."

    try:
        from pynput import keyboard

        current_keys = set()

        def on_press(key):
            try:
                current_keys.add(key)
                combo = _get_combo(current_keys)
                if combo in _hotkeys:
                    action = _hotkeys[combo]["action"]
                    msg    = f"Hotkey triggered: {combo} → {action}, sir."
                    print(f"\n⌨️  {msg}")
                    cb = _hotkeys[combo].get("callback") or callback
                    if cb:
                        cb(action)
            except Exception:
                pass

        def on_release(key):
            try:
                current_keys.discard(key)
            except Exception:
                pass

        _listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        _listener.daemon = True
        _listener.start()
        _running = True
        return "Global hotkey listener started, sir."
    except ImportError:
        return "pynput not installed. Run: pip install pynput"
    except Exception as e:
        return f"Hotkey listener failed: {e}"


def stop_hotkey_listener() -> str:
    global _running, _listener
    _running = False
    if _listener:
        try:
            _listener.stop()
        except Exception:
            pass
    return "Hotkey listener stopped, sir."


def _get_combo(keys) -> str:
    """Convert a set of pressed keys to a combo string."""
    try:
        from pynput.keyboard import Key
        parts = []
        if Key.ctrl in keys or Key.ctrl_l in keys or Key.ctrl_r in keys:
            parts.append("ctrl")
        if Key.shift in keys or Key.shift_l in keys or Key.shift_r in keys:
            parts.append("shift")
        if Key.alt in keys or Key.alt_l in keys or Key.alt_r in keys:
            parts.append("alt")
        if Key.cmd in keys or Key.cmd_l in keys:
            parts.append("cmd")
        for k in keys:
            if hasattr(k, "char") and k.char:
                parts.append(k.char.lower())
        return "+".join(parts)
    except Exception:
        return ""


def list_hotkeys() -> str:
    if not _hotkeys:
        return "No hotkeys registered, sir."
    parts = [f"'{k}' → {v['action']}" for k, v in _hotkeys.items()]
    return "Registered hotkeys: " + " | ".join(parts) + ", sir."
