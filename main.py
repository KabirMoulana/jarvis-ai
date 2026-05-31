"""
main.py — Jarvis AI entry point
Wires together all modules: listener, speaker, router, skills, memory, LLM.
"""
import sys
from jarvis.voice.listener  import Listener
from jarvis.voice.speaker   import Speaker
from jarvis.brain.ollama_client  import OllamaClient
from jarvis.brain.command_router import CommandRouter
from jarvis.memory.conversation  import ConversationMemory
from jarvis.skills import system_skills as sys_skills
from jarvis.skills import web_skills
from jarvis.config import WAKE_WORD


def run():
    print("=" * 50)
    print("  🤖  JARVIS AI  — starting up")
    print("=" * 50)

    listener = Listener()
    speaker  = Speaker()
    router   = CommandRouter()
    memory   = ConversationMemory()
    llm      = OllamaClient()

    # Calibrate mic once at startup
    listener.calibrate()

    # Check LLM availability
    if llm.is_available():
        print(f"[Jarvis] LLM online — model: {llm.model}")
    else:
        print("[Jarvis] Warning: Ollama not reachable. LLM responses disabled.")

    speaker.speak("Jarvis online. How can I help you?")

    while True:
        text = listener.listen()
        if text is None:
            continue

        routed = router.route(text)
        intent = routed["intent"]
        args   = routed["args"]

        # ── built-in instant handlers ─────────────────────────────────────────
        builtin = router.handle_builtin(routed)
        if builtin == "__exit__":
            speaker.speak("Goodbye!")
            sys.exit(0)
        if builtin:
            speaker.speak(builtin)
            memory.add("user", text)
            memory.add("assistant", builtin)
            continue

        # ── skill dispatch ────────────────────────────────────────────────────
        response = None

        if intent == "web_search" and args:
            response = web_skills.web_search(args[0])

        elif intent == "wikipedia" and args:
            response = web_skills.wikipedia_summary(args[0])

        elif intent == "weather":
            loc = args[0] if args else ""
            response = web_skills.get_weather(loc)

        elif intent == "open_url" and args:
            response = web_skills.open_url(args[0])

        elif intent == "open_app" and args:
            response = sys_skills.open_application(args[0])

        elif intent == "set_volume" and args:
            response = sys_skills.set_volume(args[0])

        elif intent == "shutdown":
            speaker.speak("Shutting down the system.")
            import subprocess
            subprocess.run(["shutdown", "-h", "now"])
            sys.exit(0)

        # ── LLM fallback ──────────────────────────────────────────────────────
        if response is None:
            if llm.is_available():
                response = llm.chat(text, history=memory.to_messages())
            else:
                response = "I'm sorry, my AI brain is offline right now."

        speaker.speak(response)
        memory.add("user", text)
        memory.add("assistant", response)


if __name__ == "__main__":
    run()
