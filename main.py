"""
main.py — J.A.R.V.I.S. v3.1 — Day 2
Full pipeline with wake word, HUD, reminders, calendar, email,
crypto/stocks, translation, and all Day 1 skills.
"""
import sys
from jarvis.boot                  import run_boot_sequence
from jarvis.hud                   import start as hud_start, stop as hud_stop, set_state
from jarvis.voice.listener        import Listener
from jarvis.voice.speaker         import Speaker
from jarvis.brain.ollama_client   import OllamaClient
from jarvis.brain.command_router  import CommandRouter
from jarvis.memory.conversation   import ConversationMemory
from jarvis.skills                import system_skills as sys_skills
from jarvis.skills                import web_skills
from jarvis.skills.vitals         import get_vitals, get_cpu, get_ram, get_battery
from jarvis.skills.briefing       import get_briefing
from jarvis.skills.timer          import set_timer, cancel_timer, list_timers, parse_duration
from jarvis.skills.news           import get_headlines
from jarvis.skills.ip_network     import get_local_ip, get_public_ip, ping_host, check_internet
from jarvis.skills.jokes          import get_joke
from jarvis.memory.note_taker     import add_note, list_notes
from jarvis.skills.reminders      import add_reminder, list_reminders, clear_reminders, parse_reminder
from jarvis.skills.calendar_skill import get_today_events, get_tomorrow_events
from jarvis.skills.email_skill    import get_unread_count, read_unread_subjects, get_latest_from
from jarvis.skills.crypto_stocks  import get_crypto_price, get_stock_price, get_market_summary
from jarvis.skills.translate      import translate
from jarvis.skills.spotify_control import (
    play_pause, next_track, previous_track,
    get_current_track, play_song
)

USE_WAKE_WORD = True   # Set False to respond to every utterance


def run():
    speaker  = Speaker()
    listener = Listener()
    router   = CommandRouter()
    memory   = ConversationMemory()
    llm      = OllamaClient()

    # ── Boot ──────────────────────────────────────────────────────────────────
    run_boot_sequence(speaker)
    hud_start()
    listener.calibrate()

    if llm.is_available():
        print(f"[Jarvis] LLM online — {llm.model}")
    else:
        print("[Jarvis] Warning: Ollama offline. LLM fallback disabled.")

    # ── Main loop ─────────────────────────────────────────────────────────────
    while True:
        # Wake word gate
        if USE_WAKE_WORD:
            set_state("idle")
            from jarvis.skills.wake_word import wait_for_wake_word
            speaker.speak("Awaiting your command, sir.")
            wait_for_wake_word()
            speaker.speak("Yes, sir?")

        set_state("listening")
        text = listener.listen()
        if text is None:
            continue

        set_state("thinking")
        routed = router.route(text)
        intent = routed["intent"]
        args   = routed["args"]

        # Built-ins
        builtin = router.handle_builtin(routed)
        if builtin == "__exit__":
            hud_stop()
            speaker.speak("Goodbye, sir. Powering down.")
            sys.exit(0)
        if builtin:
            speaker.speak(builtin)
            memory.add("user", text); memory.add("assistant", builtin)
            continue

        response = None

        # ── Briefing ──────────────────────────────────────────────────────────
        if intent == "briefing":
            response = get_briefing()

        # ── Reminders ─────────────────────────────────────────────────────────
        elif intent == "set_reminder":
            msg, when = parse_reminder(text)
            if when:
                response = add_reminder(msg, when, callback=speaker.speak)
            else:
                response = "I couldn't determine when to remind you, sir. Try 'remind me at 3pm to call John'."

        elif intent == "list_reminders":
            response = list_reminders()

        elif intent == "clear_reminders":
            response = clear_reminders()

        # ── Calendar ──────────────────────────────────────────────────────────
        elif intent == "calendar_today":
            response = get_today_events()

        elif intent == "calendar_tomorrow":
            response = get_tomorrow_events()

        # ── Email ─────────────────────────────────────────────────────────────
        elif intent == "email_count":
            response = get_unread_count()

        elif intent == "email_unread":
            response = read_unread_subjects()

        elif intent == "email_from" and args:
            response = get_latest_from(args[0])

        # ── Crypto / Stocks ───────────────────────────────────────────────────
        elif intent == "crypto_pric":
            coin = next((a for a in args if a), "bitcoin")
            response = get_crypto_price(coin)

        elif intent == "stock_price":
            ticker = next((a for a in args if a and len(a) <= 5), "AAPL")
            response = get_stock_price(ticker.upper())

        elif intent == "market_summary":
            response = get_market_summary()

        # ── Translation ───────────────────────────────────────────────────────
        elif intent == "translate" and len(args) >= 2:
            response = translate(args[0], args[1])

        # ── System vitals ─────────────────────────────────────────────────────
        elif intent == "vitals":
            kw = args[0].lower() if args else ""
            if "cpu" in kw:      response = get_cpu()
            elif "ram" in kw or "memory" in kw: response = get_ram()
            elif "battery" in kw: response = get_battery()
            else:                response = get_vitals()

        # ── Timer ─────────────────────────────────────────────────────────────
        elif intent == "set_timer":
            secs  = parse_duration(text)
            label = _extract_timer_label(text)
            response = set_timer(secs, label, callback=speaker.speak) if secs > 0 \
                else "I couldn't determine the duration, sir."
        elif intent == "cancel_timer": response = cancel_timer()
        elif intent == "list_timers":  response = list_timers()

        # ── News ──────────────────────────────────────────────────────────────
        elif intent == "news":
            cat = (args[-1].strip() if args else "") or "world"
            response = get_headlines(cat)

        # ── Network ───────────────────────────────────────────────────────────
        elif intent == "ip_local":       response = get_local_ip()
        elif intent == "ip_public":      response = get_public_ip()
        elif intent == "ping":           response = ping_host(args[0]) if args else "Specify a host, sir."
        elif intent == "internet_check": response = check_internet()

        # ── Spotify ───────────────────────────────────────────────────────────
        elif intent == "spotify_playpause": response = play_pause()
        elif intent == "spotify_next":      response = next_track()
        elif intent == "spotify_prev":      response = previous_track()
        elif intent == "spotify_current":   response = get_current_track()
        elif intent == "spotify_play_song" and args:
            response = play_song(args[0])

        # ── Web ───────────────────────────────────────────────────────────────
        elif intent == "web_search" and args:    response = web_skills.web_search(args[0])
        elif intent == "wikipedia" and args:      response = web_skills.wikipedia_summary(args[0])
        elif intent == "weather":
            loc = args[0].strip() if args else ""
            response = web_skills.get_weather(loc)
        elif intent == "open_url" and args:       response = web_skills.open_url(args[0])

        # ── System ────────────────────────────────────────────────────────────
        elif intent == "open_app" and args:       response = sys_skills.open_application(args[0])
        elif intent == "set_volume" and args:     response = sys_skills.set_volume(args[0])
        elif intent == "screenshot":              response = sys_skills.take_screenshot()

        # ── Notes ─────────────────────────────────────────────────────────────
        elif intent == "joke":                    response = get_joke()
        elif intent == "add_note" and args:       response = add_note(args[-1])
        elif intent == "list_notes":              response = list_notes()

        # ── LLM fallback ──────────────────────────────────────────────────────
        if response is None:
            set_state("thinking", "Consulting LLM ...")
            response = llm.chat(text, history=memory.to_messages()) if llm.is_available() \
                else "My AI brain is offline, sir. Ollama is not reachable."

        speaker.speak(response)
        memory.add("user", text)
        memory.add("assistant", response)


def _extract_timer_label(text: str) -> str:
    import re
    m = re.search(r"(?:set(?: a)?|start(?: a)?)\s+([\w\s]+?)\s+timer", text, re.I)
    if m:
        label = m.group(1).strip()
        if label not in ("", "a", "the"):
            return label
    return "timer"


if __name__ == "__main__":
    run()
