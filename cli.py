
"""Text-mode CLI for Jarvis — no microphone needed."""
import os
from dotenv import load_dotenv

load_dotenv()

from commands.router import route

JARVIS_NAME = os.getenv("JARVIS_NAME", "Jarvis")


def main():
    print(f"🤖 {JARVIS_NAME} CLI Mode — type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not user_input:
            continue
        response = route(user_input)
        print(f"{JARVIS_NAME}: {response}\n")
        if response == "exit":
            break


if __name__ == "__main__":
    main()
