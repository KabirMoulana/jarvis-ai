"""
jarvis/voice/listener.py
Handles all microphone input with noise calibration,
configurable energy threshold and phrase timeout.
"""
import speech_recognition as sr
from jarvis.config import (
    ENERGY_THRESHOLD,
    PAUSE_THRESHOLD,
    PHRASE_TIMEOUT,
    NOISE_CALIBRATE_SECS,
)


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold  = ENERGY_THRESHOLD
        self.recognizer.pause_threshold   = PAUSE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True

    def calibrate(self):
        """Calibrate microphone for ambient noise."""
        with sr.Microphone() as source:
            print("[Listener] Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=NOISE_CALIBRATE_SECS)
            print(f"[Listener] Energy threshold set to {self.recognizer.energy_threshold:.0f}")

    def listen(self) -> str | None:
        """
        Capture one utterance from the microphone.
        Returns the transcribed string, or None on failure.
        """
        with sr.Microphone() as source:
            print("🎤  Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=PHRASE_TIMEOUT)
            except sr.WaitTimeoutError:
                print("[Listener] No speech detected within timeout.")
                return None

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"   You said: {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("[Listener] Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"[Listener] Google STT error: {e}")
            return None

    def listen_once_raw(self) -> bytes | None:
        """Return raw audio bytes (useful for offline STT later)."""
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=PHRASE_TIMEOUT)
                return audio.get_wav_data()
            except sr.WaitTimeoutError:
                return None
