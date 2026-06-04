"""
jarvis/skills/random_generators.py
Random generators — JARVIS generates random names, numbers,
colors, decisions, and more for when you can't decide.
"""
import random
import secrets


_MALE_NAMES   = ["James","Oliver","Noah","Liam","Ethan","Lucas","Mason","Aiden","Elijah","Logan"]
_FEMALE_NAMES = ["Emma","Olivia","Ava","Isabella","Sophia","Mia","Charlotte","Amelia","Harper","Evelyn"]
_LAST_NAMES   = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Moore"]
_ADJECTIVES   = ["swift","bold","bright","dark","electric","silent","cosmic","iron","golden","quantum"]
_NOUNS        = ["falcon","phoenix","viper","titan","nova","nexus","cipher","vector","pulse","storm"]


def random_number(low: int = 1, high: int = 100) -> str:
    n = random.randint(low, high)
    return f"Your random number is {n}, sir."


def random_name(gender: str = "any") -> str:
    last = random.choice(_LAST_NAMES)
    if gender.lower() == "male":
        return f"How about {random.choice(_MALE_NAMES)} {last}, sir?"
    elif gender.lower() == "female":
        return f"How about {random.choice(_FEMALE_NAMES)} {last}, sir?"
    pool = _MALE_NAMES + _FEMALE_NAMES
    return f"How about {random.choice(pool)} {last}, sir?"


def random_codename() -> str:
    name = f"{random.choice(_ADJECTIVES).capitalize()} {random.choice(_NOUNS).capitalize()}"
    return f"Codename: {name}, sir."


def flip_coin() -> str:
    result = random.choice(["Heads", "Tails"])
    return f"{result}, sir."


def roll_dice(sides: int = 6, count: int = 1) -> str:
    rolls  = [random.randint(1, sides) for _ in range(min(count, 10))]
    total  = sum(rolls)
    if count == 1:
        return f"You rolled a {rolls[0]}, sir."
    return f"Rolled {count}d{sides}: {rolls} — total {total}, sir."


def random_color() -> str:
    r, g, b = secrets.randbelow(256), secrets.randbelow(256), secrets.randbelow(256)
    hex_c   = f"#{r:02X}{g:02X}{b:02X}"
    return f"Random color: {hex_c} (RGB: {r}, {g}, {b}), sir."


def pick_from(options: list[str]) -> str:
    if not options:
        return "No options provided, sir."
    choice = random.choice(options)
    return f"I choose '{choice}', sir."


def random_uuid() -> str:
    import uuid
    return f"Generated UUID: {uuid.uuid4()}, sir."


def random_fact_number() -> str:
    n = random.randint(1, 9999)
    return f"Random number: {n}. " + f"Fun fact: {n} is {'even' if n % 2 == 0 else 'odd'}, sir."


def magic_8ball(question: str = "") -> str:
    answers = [
        "It is certain.", "Without a doubt.", "Yes, definitely.",
        "You may rely on it.", "As I see it, yes.", "Most likely.",
        "Outlook good.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful.",
    ]
    return f"Magic 8-Ball says: {random.choice(answers)}, sir."
