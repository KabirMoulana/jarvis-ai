"""
jarvis/skills/joke_generator.py
Advanced joke engine — JARVIS tells jokes by category,
generates puns, and delivers in a dry, Iron Man style.
"""
import urllib.request
import json
import random


_LOCAL_JOKES = {
    "programming": [
        ("Why do programmers prefer dark mode?", "Because light attracts bugs, sir."),
        ("Why did the programmer quit his job?", "Because he didn't get arrays, sir."),
        ("How many programmers does it take to change a light bulb?", "None. That's a hardware problem, sir."),
        ("Why do Java developers wear glasses?", "Because they don't C#, sir."),
        ("What is a computer's favourite snack?", "Microchips, sir."),
    ],
    "science": [
        ("Why can't you trust an atom?", "They make up everything, sir."),
        ("I would tell a chemistry joke", "but I know I wouldn't get a reaction, sir."),
        ("What did the photon say when asked if it needed help with its luggage?", "No thanks, I'm travelling light, sir."),
        ("Why did the physics teacher break up with the biology teacher?", "There was no chemistry, sir."),
    ],
    "iron man": [
        ("Why does Tony Stark never use an umbrella?", "Because he has a suit for everything, sir."),
        ("What did JARVIS say when Tony asked for directions?", "Calculating... and questioning your life choices, sir."),
        ("Why doesn't Iron Man ever get lost?", "He always has a Pepper to guide him, sir."),
        ("Why did Tony Stark invest in a bakery?", "He wanted to make a lot of dough, sir."),
    ],
    "dad": [
        ("I told my wife she was drawing her eyebrows too high.", "She looked surprised, sir."),
        ("What do you call a fake noodle?", "An impasta, sir."),
        ("I'm reading a book about anti-gravity.", "It's impossible to put down, sir."),
        ("Did you hear about the mathematician who's afraid of negative numbers?", "He'll stop at nothing to avoid them, sir."),
    ],
}


def get_joke_by_category(category: str = "") -> str:
    """Return a joke from a specific category."""
    if category:
        for key in _LOCAL_JOKES:
            if category.lower() in key:
                setup, punchline = random.choice(_LOCAL_JOKES[key])
                return f"{setup} {punchline}"

    all_jokes = [j for jokes in _LOCAL_JOKES.values() for j in jokes]
    setup, punchline = random.choice(all_jokes)
    return f"{setup} {punchline}"


def get_two_part_joke() -> tuple[str, str]:
    """Return (setup, punchline) for dramatic delivery."""
    all_jokes = [j for jokes in _LOCAL_JOKES.values() for j in jokes]
    return random.choice(all_jokes)


def fetch_online_joke() -> str:
    """Fetch a fresh joke from an API."""
    try:
        url = "https://official-joke-api.appspot.com/jokes/random"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        return f"{data['setup']} {data['punchline']}, sir."
    except Exception:
        return get_joke_by_category()


def generate_pun(word: str) -> str:
    """Generate a simple pun around a word."""
    puns = {
        "time":  "I tried to catch some fog earlier. I mist, sir.",
        "money": "I used to be a banker, but I lost interest, sir.",
        "music": "I'm reading a book on the history of glue. I just can't seem to put it down, sir.",
        "code":  "A programmer's wife says 'go to the store, get a gallon of milk, and if they have eggs, get a dozen.' He comes back with 12 gallons of milk, sir.",
    }
    return puns.get(word.lower(), f"I'm still working on my {word} puns, sir. Check back later.")


def list_categories() -> str:
    return f"Joke categories: {', '.join(_LOCAL_JOKES.keys())}, sir."
