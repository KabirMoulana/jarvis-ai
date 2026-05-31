"""
main.py — J.A.R.V.I.S. v3.0 entry point
Full pipeline: boot → listen → route → skills/LLM → speak → memory
"""
import sys
from jarvis.boot                 import run_boot_sequence
from jarvis.voice.listener       import Listener
from jarvis.voice.speaker        import Speaker
from jarvis.brain.ollama_client  import OllamaClient
from jarvis.brain.command_router import CommandRouter
from jarvis.memory.conversation  import ConversationMemory
from jarvis.skills               import system_skills as sys_skills
from jarvis.skills               import web_skills
from jarvis.skills.vitals        import get_vitals, get_cpu, get_ram, get_battery
from jarvis.skills.briefing      import get_briefing
from jarvis.skills.timer         import set_timer, cancel_timer, list_timers, parse_duration
from jarvis.skills.news          import get_headlines
from jarvis.skills.ip_network    import get_local_ip, get_public_ip, ping_host, check_internet
from jarvis.skills.jokes         import get_joke
from jarvis.memory.note_taker    import add_note, list_notes


def run():
    speaker  = Speaker()
    listener = Listener()
    router   = CommandRouter()
    memory   = ConversationMemory()
    llm      = OllamaClient()

    # ── Boot ──────────────────────────────────────────────────────────────────
    run_boot_sequence(speaker)
    listener.calibrate()

    if llm.is_available():
        print(f"[Jarvis] LLM online — model: {llm.model}")
    else:
        print("[Jarvis] Warning: Ollama not reachable. LLM responses disabled.")

    # ── Main loop ─────────────────────────────────────────────────────────────
    while True:
        text = listener.listen()
        if text is None:
            continue

        routed = router.route(text)
        intent = routed["intent"]
        args   = routed["args"]

        # Built-ins (time, date, exit)
        builtin = router.handle_builtin(routed)
        if builtin == "__exit__":
            speaker.speak("Goodbye, sir. Stay safe.")
            sys.exit(0)
        if builtin:
            speaker.speak(builtin)
            memory.add("user", text)
            memory.add("assistant", builtin)
            continue

        response = None

        # ── Briefing ──────────────────────────────────────────────────────────
        if intent == "briefing":
            response = get_briefing()

        # ── System vitals ─────────────────────────────────────────────────────
        elif intent == "vitals":
            keyword = args[0].lower() if args else ""
            if "cpu" in keyword:
                response = get_cpu()
            elif "ram" in keyword or "memory" in keyword:
                response = get_ram()
            elif "battery" in keyword:
                response = get_battery()
            else:
                response = get_vitals()

        # ── Timer ─────────────────────────────────────────────────────────────
        elif intent == "set_timer":
            secs  = parse_duration(text)
            label = _extract_timer_label(text)
            if secs > 0:
                response = set_timer(secs, label, callback=speaker.speak)
            else:
                response = "I couldn't determine the duration, sir. Please say something like 'set a timer for 5 minutes'."

        elif intent == "cancel_timer":
            response = cancel_timer()

        elif intent == "list_timers":
            response = list_timers()

        # ── News ──────────────────────────────────────────────────────────────
        elif intent == "news":
            category = args[-1].strip() if args else "world"
            if not category:
                category = "world"
            response = get_headlines(category)

        # ── Network ───────────────────────────────────────────────────────────
        elif intent == "ip_local":
            response = get_local_ip()
        elif intent == "ip_public":
            response = get_public_ip()
        elif intent == "ping":
            response = ping_host(args[0]) if args else "Please specify a host to ping, sir."
        elif intent == "internet_check":
            response = check_internet()

        # ── Web / Search ──────────────────────────────────────────────────────
        elif intent == "web_search" and args:
            response = web_skills.web_search(args[0])
        elif intent == "wikipedia" and args:
            response = web_skills.wikipedia_summary(args[0])
        elif intent == "weather":
            loc = args[0].strip() if args else ""
            response = web_skills.get_weather(loc)
        elif intent == "open_url" and args:
            response = web_skills.open_url(args[0])

        # ── System ────────────────────────────────────────────────────────────
        elif intent == "open_app" and args:
            response = sys_skills.open_application(args[0])
        elif intent == "set_volume" and args:
            response = sys_skills.set_volume(args[0])
        elif intent == "screenshot":
            response = sys_skills.take_screenshot()
        elif intent == "clipboard_read":
            response = sys_skills.read_clipboard()
        elif intent == "shutdown":
            speaker.speak("Initiating shutdown sequence, sir.")
            import subprocess; subprocess.run(["shutdown", "-h", "now"])
            sys.exit(0)

        # ── Jokes ─────────────────────────────────────────────────────────────
        elif intent == "joke":
            response = get_joke()

        # ── Notes ─────────────────────────────────────────────────────────────
        elif intent == "add_note" and args:
            response = add_note(args[-1])
        elif intent == "list_notes":
            response = list_notes()

        # ── LLM fallback ──────────────────────────────────────────────────────
        if response is None:
            if llm.is_available():
                response = llm.chat(text, history=memory.to_messages())
            else:
                response = "I'm afraid my AI brain is offline right now, sir."

        speaker.speak(response)
        memory.add("user", text)
        memory.add("assistant", response)


def _extract_timer_label(text: str) -> str:
    """Try to extract a human label like 'pasta' from 'set a pasta timer for 10 minutes'."""
    import re
    m = re.search(r"(?:set(?: a)?|start(?: a)?)\s+([\w\s]+?)\s+timer", text, re.IGNORECASE)
    if m:
        label = m.group(1).strip()
        if label not in ("", "a", "the"):
            return label
    return "timer"


if __name__ == "__main__":
    run()
