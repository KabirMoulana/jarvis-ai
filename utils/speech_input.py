
"""Speech recognition utilities."""
import speech_recognition as sr


class SpeechListener:
    def __init__(self, energy_threshold: int = 300, pause_threshold: float = 0.8):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold

    def listen(self, timeout: int = 5) -> str | None:
        """Listen from the microphone and return recognized text, or None on failure."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🎤 Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text
            except sr.WaitTimeoutError:
                print("No speech detected.")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Speech service error: {e}")
                return None
