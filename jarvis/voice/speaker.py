"""
jarvis/voice/speaker.py
Text-to-speech — uses pyttsx3 with the best available voice.
Integrates with the HUD to update state during speech.
"""
import pyttsx3
import os
from jarvis.skills.voice_profile import build_engine


class Speaker:
    def __init__(self):
        self._engine = build_engine()

    def speak(self, text: str):
        if not text:
            return
        print(f"\nJarvis: {text}\n")
        try:
            # Update HUD if available
            try:
                from jarvis import hud
                hud.set_state("speaking", text[:40] + "..." if len(text) > 40 else text)
            except Exception:
                pass

            self._engine.say(text)
            self._engine.runAndWait()

            try:
                from jarvis import hud
                hud.set_state("idle")
            except Exception:
                pass
        except Exception as e:
            print(f"[Speaker] TTS error: {e}")
            # Reinitialise engine on failure
            try:
                self._engine = build_engine()
            except Exception:
                pass

    def set_rate(self, rate: int):
        self._engine.setProperty("rate", rate)

    def set_volume(self, volume: float):
        self._engine.setProperty("volume", max(0.0, min(1.0, volume)))
