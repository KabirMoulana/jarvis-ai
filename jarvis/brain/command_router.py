"""
jarvis/brain/command_router.py
Intent detection and skill dispatch.
Maps natural-language commands to the right skill handler
before falling through to the LLM.
"""
import re
from datetime import datetime


# ── intent patterns ────────────────────────────────────────────────────────────
# Each entry: (regex_pattern, intent_label)
INTENT_PATTERNS = [
    # Time / Date
    (r"\bwhat(?:'s| is)(?: the)? time\b",          "get_time"),
    (r"\bwhat(?:'s| is)(?: the)? date\b",          "get_date"),
    (r"\bwhat day is (it|today)\b",                  "get_date"),

    # System
    (r"\b(shutdown|shut down|power off)\b",         "shutdown"),
    (r"\b(restart|reboot)\b",                       "restart"),
    (r"\bopen (.+)",                                  "open_app"),
    (r"\blaunch (.+)",                                "open_app"),
    (r"\bvolume (up|down|mute|\d+)\b",             "set_volume"),

    # Web / Search
    (r"\bsearch(?: for)? (.+)",                       "web_search"),
    (r"\bgoogle (.+)",                                "web_search"),
    (r"\bwikipedia (.+)",                             "wikipedia"),
    (r"\btell me about (.+)",                         "wikipedia"),
    (r"\bopen (https?://\S+)",                       "open_url"),

    # Weather
    (r"\bweather(?: in| for)? ?(.*)\b",             "weather"),

    # Jokes / Fun
    (r"\btell me a joke\b",                          "joke"),
    (r"\bsay something funny\b",                     "joke"),

    # Exit
    (r"\b(exit|quit|bye|goodbye|stop|shut up)\b",   "exit"),
]

_COMPILED = [(re.compile(p, re.IGNORECASE), label) for p, label in INTENT_PATTERNS]


class CommandRouter:
    """
    Route a raw text command to an intent + extracted args.
    Returns a dict: {"intent": str, "args": list[str], "raw": str}
    """

    def route(self, command: str) -> dict:
        command = command.strip()
        for pattern, label in _COMPILED:
            m = pattern.search(command)
            if m:
                args = [g for g in m.groups() if g is not None]
                return {"intent": label, "args": args, "raw": command}
        # No rule matched → send to LLM
        return {"intent": "llm", "args": [], "raw": command}

    # ── built-in handlers (no external deps) ─────────────────────────────────

    def handle_builtin(self, routed: dict) -> str | None:
        """
        Handle simple intents that don't need the LLM or skills.
        Returns a string response, or None if not a builtin.
        """
        intent = routed["intent"]
        args   = routed["args"]

        if intent == "get_time":
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."

        if intent == "get_date":
            return f"Today is {datetime.now().strftime('%A, %B %d %Y')}."

        if intent == "exit":
            return "__exit__"

        return None   # let skill layer / LLM handle it
