"""
jarvis/skills/gui_hud.py
GUI HUD overlay — Iron Man style floating window using tkinter.
Shows: clock, system vitals, JARVIS status, last response.
Runs in a background thread so it doesn't block the main loop.
"""
import threading
import time
from datetime import datetime

_hud_thread = None
_running    = False
_status_var = None
_response_var = None
_root       = None


def launch_hud():
    """Launch the JARVIS GUI HUD in a background thread."""
    global _hud_thread, _running
    if _running:
        return "HUD is already running, sir."
    _running    = True
    _hud_thread = threading.Thread(target=_run_hud, daemon=True)
    _hud_thread.start()
    return "HUD overlay activated, sir."


def close_hud():
    global _running, _root
    _running = False
    if _root:
        try:
            _root.destroy()
        except Exception:
            pass
    return "HUD overlay closed, sir."


def update_status(text: str):
    global _status_var
    if _status_var:
        try:
            _status_var.set(text)
        except Exception:
            pass


def update_response(text: str):
    global _response_var
    if _response_var:
        try:
            _response_var.set(text[:80] + "..." if len(text) > 80 else text)
        except Exception:
            pass


def _run_hud():
    global _root, _status_var, _response_var
    try:
        import tkinter as tk
        from tkinter import font as tkfont

        _root = tk.Tk()
        _root.title("J.A.R.V.I.S")
        _root.geometry("420x280+20+20")
        _root.configure(bg="#0a0a0a")
        _root.attributes("-topmost", True)
        _root.attributes("-alpha", 0.92)
        _root.overrideredirect(True)   # Borderless window

        # ── Fonts ──────────────────────────────────────────────────────────
        font_big   = tkfont.Font(family="Courier", size=22, weight="bold")
        font_med   = tkfont.Font(family="Courier", size=11)
        font_small = tkfont.Font(family="Courier", size=9)

        CYAN  = "#00d4ff"
        DIM   = "#005a6e"
        WHITE = "#e0f7ff"
        BG    = "#0a0a0a"

        # ── Header ─────────────────────────────────────────────────────────
        tk.Label(_root, text="◈  J.A.R.V.I.S  ◈", bg=BG, fg=CYAN,
                 font=font_med).pack(pady=(12, 0))
        tk.Frame(_root, bg=DIM, height=1).pack(fill="x", padx=20, pady=4)

        # ── Clock ──────────────────────────────────────────────────────────
        clock_var = tk.StringVar()
        tk.Label(_root, textvariable=clock_var, bg=BG, fg=CYAN,
                 font=font_big).pack()

        # ── Date ───────────────────────────────────────────────────────────
        date_var = tk.StringVar()
        tk.Label(_root, textvariable=date_var, bg=BG, fg=DIM,
                 font=font_small).pack()

        tk.Frame(_root, bg=DIM, height=1).pack(fill="x", padx=20, pady=6)

        # ── Status ─────────────────────────────────────────────────────────
        _status_var = tk.StringVar(value="◉  Standing by ...")
        tk.Label(_root, textvariable=_status_var, bg=BG, fg=WHITE,
                 font=font_small).pack()

        # ── Last response ──────────────────────────────────────────────────
        _response_var = tk.StringVar(value="")
        tk.Label(_root, textvariable=_response_var, bg=BG, fg=DIM,
                 font=font_small, wraplength=380).pack(pady=(4, 0))

        tk.Frame(_root, bg=DIM, height=1).pack(fill="x", padx=20, pady=6)

        # ── Vitals bar ─────────────────────────────────────────────────────
        vitals_var = tk.StringVar(value="CPU: --%  RAM: --%  BAT: --%")
        tk.Label(_root, textvariable=vitals_var, bg=BG, fg=DIM,
                 font=font_small).pack()

        # ── Close button ───────────────────────────────────────────────────
        tk.Button(_root, text="✕", bg=BG, fg=DIM, bd=0,
                  command=_root.destroy).place(x=395, y=5)

        def _tick():
            if not _running:
                _root.destroy()
                return
            now = datetime.now()
            clock_var.set(now.strftime("%H:%M:%S"))
            date_var.set(now.strftime("%A  %d %B %Y"))
            # Update vitals every 5 seconds
            if now.second % 5 == 0:
                try:
                    import psutil
                    cpu = psutil.cpu_percent()
                    ram = psutil.virtual_memory().percent
                    bat = psutil.sensors_battery()
                    bat_str = f"{bat.percent:.0f}%" if bat else "N/A"
                    vitals_var.set(f"CPU: {cpu:.0f}%  RAM: {ram:.0f}%  BAT: {bat_str}")
                except Exception:
                    pass
            _root.after(1000, _tick)

        _tick()
        _root.mainloop()
    except Exception as e:
        print(f"[HUD] GUI error: {e}")
