"""
jarvis/voice/speaker.py
Text-to-speech with platform auto-detection.
  - macOS  → native `say` command (zero deps)
  - others → pyttsx3 (pip install pyttsx3)
Falls back to print-only if neither is available.
"""
import os
import sys
import subprocess
from jarvis.config import TTS_RATE, TTS_VOLUME


class Speaker:
    def __init__(self):
        self._engine   = None
        self._platform = sys.platform
        self._init_engine()

    def _init_engine(self):
        if self._platform == "darwin":
            self._mode = "macos"
            return
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate",   TTS_RATE)
            engine.setProperty("volume", TTS_VOLUME)
            self._engine = engine
            self._mode   = "pyttsx3"
        except Exception:
            self._mode = "print"
            print("[Speaker] Warning: no TTS engine found. Using print-only mode.")

    def speak(self, text: str):
        """Speak the given text aloud."""
        print(f"Jarvis: {text}")
        if self._mode == "macos":
            # Escape double-quotes to avoid shell injection
            safe = text.replace('"', '\"')
            subprocess.run(["say", safe], check=False)
        elif self._mode == "pyttsx3":
            self._engine.say(text)
            self._engine.runAndWait()
        # print-only mode already printed above

    def set_voice(self, voice_id: str):
        """Change pyttsx3 voice by ID (no-op on macOS)."""
        if self._mode == "pyttsx3" and self._engine:
            self._engine.setProperty("voice", voice_id)

    def list_voices(self) -> list[str]:
        """Return available pyttsx3 voice IDs."""
        if self._mode == "pyttsx3" and self._engine:
            return [v.id for v in self._engine.getProperty("voices")]
        return []
