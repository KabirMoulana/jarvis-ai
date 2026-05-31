"""
jarvis/skills/jokes.py
Joke skill — fetches a random joke from the free
icanhazdadjoke API (no key required) with a local
fallback list if the network is unavailable.
"""
import urllib.request
import json
import random

_FALLBACK_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
]

def get_joke() -> str:
    """Fetch a random joke. Falls back to local list on network error."""
    try:
        req = urllib.request.Request(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json", "User-Agent": "JarvisAI/0.2"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return data.get("joke", random.choice(_FALLBACK_JOKES))
    except Exception:
        return random.choice(_FALLBACK_JOKES)
