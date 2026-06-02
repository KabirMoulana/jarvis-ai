"""
jarvis/skills/voice_commands_help.py
Help system — JARVIS lists all available voice commands
grouped by category. Spoken or printed on request.
"""

COMMANDS = {
    "Time & Date": [
        "What time is it?",
        "What's the date?",
        "What day is today?",
    ],
    "Briefing": [
        "Morning briefing",
        "Daily briefing",
        "Good morning",
    ],
    "System": [
        "System status",
        "How's my CPU?",
        "Check battery",
        "Check RAM",
        "Take a screenshot",
        "Read my clipboard",
        "Open [app name]",
        "Volume up / down / mute",
    ],
    "Timers & Reminders": [
        "Set a timer for 10 minutes",
        "Set a pasta timer for 20 minutes",
        "Cancel the timer",
        "Remind me at 3pm to call John",
        "Remind me in 30 minutes to check email",
        "List my reminders",
        "Clear all reminders",
    ],
    "Calendar & Email": [
        "What's on my schedule today?",
        "What's happening tomorrow?",
        "Check my email",
        "Read my unread emails",
        "Latest email from [name]",
    ],
    "News & Weather": [
        "What's the news?",
        "Tech headlines",
        "World news",
        "Weather in London",
        "Weather in New York",
    ],
    "Finance": [
        "Bitcoin price",
        "Ethereum price",
        "How is AAPL doing?",
        "Tesla stock",
        "Market summary",
    ],
    "Music": [
        "Play",
        "Pause",
        "Next track",
        "Previous track",
        "What song is this?",
        "Play [song name] on Spotify",
    ],
    "Network": [
        "What's my IP address?",
        "Public IP",
        "Ping google.com",
        "Check internet",
        "Run a speed test",
    ],
    "Productivity": [
        "Start focus mode for 25 minutes",
        "Stop focus mode",
        "Focus status",
        "Note that [message]",
        "Show my notes",
    ],
    "Translation": [
        "Translate hello to French",
        "How do you say goodbye in Japanese?",
    ],
    "Search": [
        "Search for [query]",
        "Google [query]",
        "Wikipedia [topic]",
        "Tell me about [topic]",
    ],
    "General": [
        "Tell me a joke",
        "Who are you?",
        "How are you?",
        "Exit / Goodbye",
    ],
}


def get_help(category: str = "") -> str:
    """Return spoken help for a category or a general overview."""
    if category:
        cat_lower = category.lower()
        for key, cmds in COMMANDS.items():
            if cat_lower in key.lower():
                return (
                    f"Here are the {key} commands, sir: "
                    + ". ".join(cmds[:5])
                    + ("." if len(cmds) <= 5 else f". And {len(cmds)-5} more.")
                )

    total = sum(len(v) for v in COMMANDS.values())
    cats  = ", ".join(COMMANDS.keys())
    return (
        f"I have {total} voice commands across {len(COMMANDS)} categories, sir. "
        f"Categories: {cats}. "
        f"Say 'help with [category]' for details."
    )


def print_all_commands():
    """Pretty-print all commands to the terminal."""
    print("\n" + "═" * 55)
    print("  J.A.R.V.I.S  —  Voice Command Reference")
    print("═" * 55)
    for category, cmds in COMMANDS.items():
        print(f"\n  ◆ {category}")
        for cmd in cmds:
            print(f"      • {cmd}")
    print("\n" + "═" * 55 + "\n")
