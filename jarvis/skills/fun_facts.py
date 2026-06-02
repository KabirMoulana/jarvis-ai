"""
jarvis/skills/fun_facts.py
Fun and interesting facts — JARVIS delivers curated facts
across science, history, technology, and Iron Man universe.
Also fetches live facts from the Numbers API.
"""
import urllib.request
import random


_FACTS = {
    "science": [
        "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible, sir.",
        "A teaspoon of a neutron star would weigh about 10 million tonnes, sir.",
        "The human brain generates about 70,000 thoughts per day, sir.",
        "Octopuses have three hearts and blue blood, sir.",
        "There are more possible iterations of a game of chess than there are atoms in the observable universe, sir.",
        "Water can boil and freeze at the same time — it's called the triple point, sir.",
        "A single bolt of lightning contains enough energy to toast 100,000 slices of bread, sir.",
    ],
    "technology": [
        "The first computer bug was an actual bug — a moth found in a Harvard Mark II relay in 1947, sir.",
        "The first 1GB hard drive, released in 1980, weighed 550 pounds and cost $40,000, sir.",
        "More people in the world have mobile phones than toilets, sir.",
        "The average person unlocks their phone 150 times per day, sir.",
        "Google processes approximately 8.5 billion searches per day, sir.",
        "The Internet weighs about 50 grams — the mass of electrons carrying the data, sir.",
        "The first email was sent in 1971 by Ray Tomlinson — to himself, sir.",
    ],
    "history": [
        "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid, sir.",
        "Oxford University is older than the Aztec Empire, sir.",
        "Napoleon was not short — he was 5 feet 7 inches, above average for his time, sir.",
        "The fax machine was invented before the telephone, sir.",
        "Vikings never actually wore horned helmets in battle, sir.",
        "Ancient Romans used crushed mouse brains as toothpaste, sir.",
    ],
    "iron man": [
        "Tony Stark built the first Iron Man suit in a cave with a box of scraps, sir.",
        "The arc reactor in Tony's chest generates 3 gigajoules per second, sir.",
        "JARVIS stands for Just A Rather Very Intelligent System, sir.",
        "The Iron Man Mark III suit is made of a titanium-gold alloy, sir.",
        "Pepper Potts' real name is Virginia Potts, sir.",
        "Tony Stark has an IQ of 270, making him one of the smartest humans alive, sir.",
        "The Hulkbuster armour weighs approximately 10 times more than a standard Iron Man suit, sir.",
    ],
    "space": [
        "One million Earths could fit inside the Sun, sir.",
        "The footprints left by Apollo astronauts will remain on the Moon for 100 million years, sir.",
        "There is a planet made mostly of diamond — 55 Cancri e — twice the size of Earth, sir.",
        "Sound cannot travel in space, but radio waves can, sir.",
        "A day on Venus is longer than a year on Venus, sir.",
    ],
}


def get_fact(category: str = "") -> str:
    """Return a random fact, optionally filtered by category."""
    if category:
        cat = category.lower().strip()
        for key in _FACTS:
            if cat in key or key in cat:
                return random.choice(_FACTS[key])

    all_facts = [f for facts in _FACTS.values() for f in facts]
    return random.choice(all_facts)


def get_number_fact(number: int | None = None) -> str:
    """Fetch an interesting fact about a number from the Numbers API."""
    num = number if number is not None else random.randint(1, 1000)
    try:
        url = f"http://numbersapi.com/{num}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            fact = resp.read().decode()
        return f"{fact}, sir."
    except Exception:
        return f"{num} is a perfectly ordinary number, sir. Nothing remarkable to report."


def get_date_fact() -> str:
    """Fetch a fact about today's date."""
    from datetime import date
    today = date.today()
    try:
        url = f"http://numbersapi.com/{today.month}/{today.day}/date"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            fact = resp.read().decode()
        return f"On this day in history — {fact}, sir."
    except Exception:
        return f"Today is {today.strftime('%B %d')}, sir. A fine day by any measure."


def list_categories() -> str:
    cats = ", ".join(_FACTS.keys())
    return f"Fact categories available: {cats}, sir."
