"""
jarvis/skills/motivation.py
Motivational quotes and productivity boosts — JARVIS style.
Pulls from a curated Iron Man / tech / stoic quote bank
plus the ZenQuotes API for fresh quotes.
"""
import urllib.request
import json
import random
from datetime import datetime

_LOCAL_QUOTES = [
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Stay hungry. Stay foolish.", "Steve Jobs"),
    ("Whether you think you can, or you think you can't — you're right.", "Henry Ford"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Do or do not. There is no try.", "Yoda"),
    ("Part of being a winner is knowing when enough is enough.", "Donald Trump"),
    ("I am Iron Man.", "Tony Stark"),
    ("Genius, billionaire, playboy, philanthropist.", "Tony Stark"),
    ("Sometimes you gotta run before you can walk.", "Tony Stark"),
    ("The measure of intelligence is the ability to change.", "Albert Einstein"),
    ("We are what we repeatedly do. Excellence is not an act but a habit.", "Aristotle"),
    ("He who has a why to live can bear almost any how.", "Nietzsche"),
    ("The obstacle is the way.", "Marcus Aurelius"),
    ("Waste no more time arguing about what a good man should be. Be one.", "Marcus Aurelius"),
    ("You have power over your mind — not outside events. Realise this and you will find strength.", "Marcus Aurelius"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("The science of today is the technology of tomorrow.", "Edward Teller"),
]


def get_quote(source: str = "local") -> str:
    """Return a motivational quote — local bank or live API."""
    if source == "api":
        api_quote = _fetch_api_quote()
        if api_quote:
            return api_quote

    quote, author = random.choice(_LOCAL_QUOTES)
    return f'"{quote}" — {author}.'


def get_daily_quote() -> str:
    """Return a consistent quote for today (same quote all day)."""
    seed  = int(datetime.now().strftime("%Y%m%d"))
    quote, author = _LOCAL_QUOTES[seed % len(_LOCAL_QUOTES)]
    return f'Your quote for today, sir: "{quote}" — {author}.'


def get_iron_man_quote() -> str:
    """Return a Tony Stark / Iron Man quote specifically."""
    stark_quotes = [q for q in _LOCAL_QUOTES if q[1] == "Tony Stark"]
    if stark_quotes:
        quote, author = random.choice(stark_quotes)
        return f'"{quote}" — {author}.'
    return get_quote()


def get_stoic_quote() -> str:
    """Return a stoic philosophy quote."""
    stoic = [q for q in _LOCAL_QUOTES if q[1] in ("Marcus Aurelius", "Nietzsche", "Aristotle")]
    if stoic:
        quote, author = random.choice(stoic)
        return f'"{quote}" — {author}.'
    return get_quote()


def _fetch_api_quote() -> str | None:
    try:
        req = urllib.request.Request(
            "https://zenquotes.io/api/random",
            headers={"User-Agent": "JarvisAI/3.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        if data and isinstance(data, list):
            q = data[0]
            return f'"{q["q"]}" — {q["a"]}.'
    except Exception:
        pass
    return None
