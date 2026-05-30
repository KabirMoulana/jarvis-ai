
"""Jarvis AI — main entry point."""
import os
from dotenv import load_dotenv

load_dotenv()

from utils.text_to_speech import speak
from utils.speech_input import SpeechListener
from commands.router import route

JARVIS_NAME = os.getenv("JARVIS_NAME", "Jarvis")


def main():
    listener = SpeechListener()
    print(f"🤖 {JARVIS_NAME} Activated — say 'exit' to quit.")
    speak(f"Hello, I am {JARVIS_NAME}. How can I help you?")

    while True:
        text = listener.listen()
        if text is None:
            continue
        response = route(text)
        if response == "exit":
            speak("Shutting down. Goodbye!")
            break
        speak(response)


if __name__ == "__main__":
    main()
