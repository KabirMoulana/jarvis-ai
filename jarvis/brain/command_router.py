"""
jarvis/brain/command_router.py
Intent detection and skill dispatch — Day 2 expanded.
"""
import re
from datetime import datetime

INTENT_PATTERNS = [
    # Time / Date
    (r"\bwhat(?:'s| is)(?: the)? time\b",                    "get_time"),
    (r"\bwhat(?:'s| is)(?: the)? date\b",                    "get_date"),
    (r"\bwhat day is (it|today)\b",                          "get_date"),

    # Briefing
    (r"\b(morning|daily|evening)\s*briefing\b",             "briefing"),
    (r"\bbriefing\b",                                        "briefing"),
    (r"\bgood morning\b",                                    "briefing"),

    # Reminders
    (r"\bremind\s+me\b",                                     "set_reminder"),
    (r"\blist(?: my)? reminders\b",                         "list_reminders"),
    (r"\bclear(?: all)? reminders\b",                       "clear_reminders"),

    # Calendar
    (r"\b(what(?:'s| is) on my|show my|check my) (calendar|schedule|agenda)\b", "calendar_today"),
    (r"\b(today(?:'s)? (schedule|events|calendar))\b",      "calendar_today"),
    (r"\btomorrow(?:'s)? (schedule|events|calendar)\b",     "calendar_tomorrow"),
    (r"\bwhat(?:'s| is) (on|happening) tomorrow\b",         "calendar_tomorrow"),

    # Email
    (r"\b(check|read)(?: my)? email\b",                     "email_unread"),
    (r"\bhow many (emails?|messages?)\b",                   "email_count"),
    (r"\b(unread|new) (emails?|messages?)\b",               "email_unread"),
    (r"\blatest email from (.+)\b",                         "email_from"),

    # Crypto / Stocks
    (r"\b(price of|how much is|what(?:'s| is)) (bitcoin|btc|ethereum|eth|solana|sol|dogecoin|doge|cardano|ada|xrp|ripple|bnb)\b", "crypto_price"),
    (r"\b(bitcoin|btc|ethereum|eth|solana|sol|dogecoin|doge) price\b", "crypto_price"),
    (r"\b(stock price of|how is|price of) ([A-Z]{1,5})\b",  "stock_price"),
    (r"\b([A-Z]{2,5}) stock\b",                             "stock_price"),
    (r"\bmarket (summary|update|overview)\b",               "market_summary"),

    # Translation
    (r"\btranslate (.+) (?:to|in(?:to)?) (\w+)\b",          "translate"),
    (r"\bhow do (?:you|i) say (.+) in (\w+)\b",             "translate"),

    # System vitals
    (r"\b(system|pc|computer)\s*(status|vitals|health|stats)\b", "vitals"),
    (r"\bhow(?:'s| is)(?: the)? (cpu|ram|memory|battery|disk)\b","vitals"),
    (r"\bcheck (cpu|ram|memory|battery|disk|system)\b",          "vitals"),

    # Timer
    (r"\bset(?: a)? timer\b",                                "set_timer"),
    (r"\btimer for\b",                                       "set_timer"),
    (r"\bremind me in\b",                                    "set_timer"),
    (r"\bcancel(?: the)? timer\b",                           "cancel_timer"),
    (r"\blist timers\b",                                     "list_timers"),

    # News
    (r"\b(news|headlines)(?: about| on| for)? ?(.*)\b",      "news"),
    (r"\bwhat(?:'s| is)(?: the)? news\b",                    "news"),
    (r"\btop stories\b",                                     "news"),

    # Network
    (r"\b(my |local )?ip address\b",                        "ip_local"),
    (r"\bpublic ip\b",                                       "ip_public"),
    (r"\bping (.+)\b",                                       "ping"),
    (r"\b(check |is there )?(internet|wifi|network|connection)\b", "internet_check"),

    # Spotify
    (r"\b(play|pause|resume)\b(?! song| track| music| next| previous)", "spotify_playpause"),
    (r"\bnext (song|track)\b",                               "spotify_next"),
    (r"\b(previous|last|back) (song|track)\b",              "spotify_prev"),
    (r"\bwhat(?:'s| is)(?: this| playing| the)? (song|track|music)\b", "spotify_current"),
    (r"\bplay (.+) on spotify\b",                            "spotify_play_song"),
    (r"\bplay (.+)\b",                                       "spotify_play_song"),

    # System
    (r"\bopen (.+)\b",                                       "open_app"),
    (r"\blaunch (.+)\b",                                     "open_app"),
    (r"\bvolume (up|down|mute|\d+)\b",                      "set_volume"),
    (r"\btake(?: a)? screenshot\b",                         "screenshot"),

    # Web / Search
    (r"\bsearch(?: for)? (.+)",                              "web_search"),
    (r"\bgoogle (.+)",                                       "web_search"),
    (r"\bwikipedia (.+)",                                    "wikipedia"),
    (r"\btell me about (.+)",                                "wikipedia"),
    (r"\bopen (https?://\S+)",                               "open_url"),

    # Weather
    (r"\bweather(?: in| for)? ?(.*)\b",                      "weather"),

    # Jokes / Notes
    (r"\btell(?: me)? a joke\b",                             "joke"),
    (r"\bnote(?: that| down)? (.+)\b",                       "add_note"),
    (r"\bremember that (.+)\b",                              "add_note"),
    (r"\bshow(?: my)? notes\b",                              "list_notes"),
    (r"\blist(?: my)? notes\b",                              "list_notes"),

    # Exit
    (r"\b(exit|quit|bye|goodbye|stop jarvis|shut up)\b",    "exit"),
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
