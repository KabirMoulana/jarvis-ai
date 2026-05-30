
"""Cross-platform text-to-speech utility."""
import sys
import os

try:
    import pyttsx3
    _engine = pyttsx3.init()
    _engine.setProperty("rate", 160)
    _USE_PYTTSX3 = True
except Exception:
    _USE_PYTTSX3 = False


def speak(text: str) -> None:
    """Speak the given text aloud."""
    print("Jarvis:", text)
    if _USE_PYTTSX3:
        _engine.say(text)
        _engine.runAndWait()
    elif sys.platform == "darwin":
        os.system(f'say "{text}"')
    else:
        print("[TTS not available on this platform]")
