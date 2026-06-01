"""
jarvis/skills/voice_profile.py
JARVIS voice profile — deeper, more robotic TTS using pyttsx3.
Selects the best available voice (prefers deep male voices).
Also provides a spoken status HUD line for the terminal.
"""
import pyttsx3
import platform
import os


_PREFERRED_VOICE_KEYWORDS = [
    "daniel",   # macOS UK English deep male
    "alex",     # macOS US English
    "fred",     # macOS robotic
    "david",    # Windows
    "mark",     # Windows
    "english",
]


def build_engine() -> pyttsx3.Engine:
    """
    Build and return a pyttsx3 engine pre-configured with
    the deepest, most JARVIS-like voice available on this system.
    """
    engine = pyttsx3.init()

    # ── Rate ──────────────────────────────────────────────────────────────────
    rate = int(os.getenv("JARVIS_TTS_RATE", "175"))
    engine.setProperty("rate", rate)

    # ── Volume ────────────────────────────────────────────────────────────────
    engine.setProperty("volume", float(os.getenv("JARVIS_TTS_VOLUME", "0.95")))

    # ── Voice selection ───────────────────────────────────────────────────────
    voices = engine.getProperty("voices")
    chosen = None

    for keyword in _PREFERRED_VOICE_KEYWORDS:
        for v in voices:
            if keyword in v.name.lower() or keyword in (v.id or "").lower():
                chosen = v
                break
        if chosen:
            break

    # Fallback: first male voice, or just the first voice
    if chosen is None:
        for v in voices:
            if hasattr(v, "gender") and v.gender == "male":
                chosen = v
                break
    if chosen is None and voices:
        chosen = voices[0]

    if chosen:
        engine.setProperty("voice", chosen.id)
        print(f"[VoiceProfile] Using voice: {chosen.name}")

    return engine


def list_available_voices() -> str:
    """Return all available voices as a spoken summary."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    names  = [v.name for v in voices]
    engine.stop()
    return f"Available voices: {', '.join(names)}."


def get_voice_info() -> str:
    """Return info about the currently selected voice."""
    engine = build_engine()
    voice_id = engine.getProperty("voice")
    rate     = engine.getProperty("rate")
    volume   = int(engine.getProperty("volume") * 100)
    engine.stop()
    return f"Voice profile: rate {rate} words per minute, volume {volume} percent."
