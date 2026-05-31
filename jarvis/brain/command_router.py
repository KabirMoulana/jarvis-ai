"""
jarvis/brain/command_router.py
Intent detection and skill dispatch.
Maps natural-language commands to the right skill handler
before falling through to the LLM.
"""
import re
from datetime import datetime


# ── intent patterns ────────────────────────────────────────────────────────────
INTENT_PATTERNS = [
    # Time / Date
    (r"\bwhat(?:'s| is)(?: the)? time\b",           "get_time"),
    (r"\bwhat(?:'s| is)(?: the)? date\b",           "get_date"),
    (r"\bwhat day is (it|today)\b",                  "get_date"),

    # Briefing
    (r"\b(morning|daily|evening)\s*briefing\b",     "briefing"),
    (r"\bbriefing\b",                                "briefing"),
    (r"\bgood morning\b",                            "briefing"),

    # System vitals
    (r"\b(system|pc|computer)\s*(status|vitals|health|stats)\b", "vitals"),
    (r"\bhow(?:'s| is)(?: the)? (cpu|ram|memory|battery|disk)\b","vitals"),
    (r"\bcheck (cpu|ram|memory|battery|disk|system)\b",          "vitals"),

    # Timer
    (r"\bset(?: a)? timer\b",                        "set_timer"),
    (r"\btimer for\b",                               "set_timer"),
    (r"\bremind me in\b",                            "set_timer"),
    (r"\bcancel(?: the)? timer\b",                   "cancel_timer"),
    (r"\blist timers\b",                             "list_timers"),

    # News
    (r"\b(news|headlines)(?: about| on| for)? ?(.*)\b", "news"),
    (r"\bwhat(?:'s| is)(?: the)? news\b",            "news"),
    (r"\btop stories\b",                             "news"),

    # Network
    (r"\b(my |local )?ip address\b",                "ip_local"),
    (r"\bpublic ip\b",                               "ip_public"),
    (r"\bping (.+)\b",                               "ping"),
    (r"\b(check |is there )?(internet|wifi|network|connection)\b", "internet_check"),

    # System
    (r"\b(shutdown|shut down|power off)\b",         "shutdown"),
    (r"\b(restart|reboot)\b",                       "restart"),
    (r"\bopen (.+)\b",                              "open_app"),
    (r"\blaunch (.+)\b",                            "open_app"),
    (r"\bvolume (up|down|mute|\d+)\b",              "set_volume"),
    (r"\btake(?: a)? screenshot\b",                 "screenshot"),
    (r"\bread(?: my)? clipboard\b",                 "clipboard_read"),

    # Web / Search
    (r"\bsearch(?: for)? (.+)",                     "web_search"),
    (r"\bgoogle (.+)",                              "web_search"),
    (r"\bwikipedia (.+)",                           "wikipedia"),
    (r"\btell me about (.+)",                       "wikipedia"),
    (r"\bopen (https?://\S+)",                      "open_url"),

    # Weather
    (r"\bweather(?: in| for)? ?(.*)\b",             "weather"),

    # Jokes
    (r"\btell(?: me)? a joke\b",                    "joke"),
    (r"\bsay something funny\b",                    "joke"),

    # Notes
    (r"\bnote(?: that| down)? (.+)\b",              "add_note"),
    (r"\bremember that (.+)\b",                     "add_note"),
    (r"\bshow(?: my)? notes\b",                     "list_notes"),
    (r"\blist(?: my)? notes\b",                     "list_notes"),

    # Exit
    (r"\b(exit|quit|bye|goodbye|stop jarvis|shut up)\b", "exit"),
]

_COMPILED = [(re.compile(p, re.IGNORECASE), label) for p, label in INTENT_PATTERNS]


class CommandRouter:
    def route(self, command: str) -> dict:
        command = command.strip()
        for pattern, label in _COMPILED:
            m = pattern.search(command)
            if m:
                args = [g for g in m.groups() if g is not None]
                return {"intent": label, "args": args, "raw": command}
        return {"intent": "llm", "args": [], "raw": command}

    def handle_builtin(self, routed: dict) -> str | None:
        intent = routed["intent"]

        if intent == "get_time":
            return f"The current time is {datetime.now().strftime('%I:%M %p')}, sir."

        if intent == "get_date":
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}, sir."

        if intent == "exit":
            return "__exit__"

        return None
