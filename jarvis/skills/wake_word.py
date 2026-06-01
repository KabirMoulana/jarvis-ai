"""
jarvis/skills/wake_word.py
Wake word detection — Jarvis only activates on "Hey Jarvis".
Runs a lightweight background listener thread.
No cloud required — uses local speech_recognition energy detection.
"""
import threading
import speech_recognition as sr
from jarvis.config import WAKE_WORD


class WakeWordDetector:
    def __init__(self, on_wake=None):
        self.on_wake   = on_wake        # callable triggered when wake word heard
        self._running  = False
        self._thread   = None
        self._r        = sr.Recognizer()
        self._r.energy_threshold        = 280
        self._r.dynamic_energy_threshold = True
        self._r.pause_threshold         = 0.6

    def start(self):
        """Start background wake-word listening thread."""
        self._running = True
        self._thread  = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print(f"[WakeWord] Listening for '{WAKE_WORD}' ...")

    def stop(self):
        self._running = False

    def _loop(self):
        with sr.Microphone() as source:
            self._r.adjust_for_ambient_noise(source, duration=1)
            while self._running:
                try:
                    audio = self._r.listen(source, timeout=3, phrase_time_limit=4)
                    text  = self._r.recognize_google(audio).lower()
                    if WAKE_WORD.lower() in text:
                        print(f"[WakeWord] Wake word detected: '{text}'")
                        if self.on_wake:
                            self.on_wake()
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"[WakeWord] Error: {e}")


def wait_for_wake_word() -> bool:
    """
    Blocking call — returns True when wake word is spoken.
    Useful for single-shot detection without a background thread.
    """
    r = sr.Recognizer()
    r.energy_threshold         = 280
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                text  = r.recognize_google(audio).lower()
                if WAKE_WORD.lower() in text:
                    return True
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                pass
            except Exception:
                return False
