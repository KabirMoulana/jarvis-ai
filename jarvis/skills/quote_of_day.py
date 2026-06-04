"""
jarvis/skills/quote_of_day.py
Quote of the day — JARVIS delivers curated quotes
for different moods and contexts: morning, productivity,
leadership, stoic, tech, and Iron Man.
"""
import random
from datetime import date

_QUOTES = {
    "morning": [
        ("Each morning we are born again. What we do today matters most.", "Buddha"),
        ("Morning is an important time of day because how you spend your morning can often tell you what kind of day you are going to have.", "Lemony Snicket"),
        ("Every morning you have two choices: continue to sleep with your dreams, or wake up and chase them.", "Unknown"),
        ("Today's goals: Coffee and kindness. Maybe two coffees, and as much kindness as possible.", "Unknown"),
    ],
    "productivity": [
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("Done is better than perfect.", "Sheryl Sandberg"),
        ("Focus on being productive instead of busy.", "Tim Ferriss"),
        ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
        ("Your time is limited, so don't waste it living someone else's life.", "Steve Jobs"),
    ],
    "leadership": [
        ("A leader is one who knows the way, goes the way, and shows the way.", "John C. Maxwell"),
        ("The function of leadership is to produce more leaders, not more followers.", "Ralph Nader"),
        ("Leadership is not about being in charge. It is about taking care of those in your charge.", "Simon Sinek"),
        ("The greatest leader is not necessarily the one who does the greatest things. He is the one that gets the people to do the greatest things.", "Ronald Reagan"),
    ],
    "stoic": [
        ("Waste no more time arguing about what a good man should be. Be one.", "Marcus Aurelius"),
        ("The impediment to action advances action. What stands in the way becomes the way.", "Marcus Aurelius"),
        ("You have power over your mind, not outside events. Realise this and you will find strength.", "Marcus Aurelius"),
        ("He who has a why to live can bear almost any how.", "Friedrich Nietzsche"),
        ("Do not seek for things to happen the way you want them to; but wish the things that happen to be as they are.", "Epictetus"),
    ],
    "tech": [
        ("The best way to predict the future is to invent it.", "Alan Kay"),
        ("Move fast and break things. Unless you are breaking stuff, you are not moving fast enough.", "Mark Zuckerberg"),
        ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("Software is eating the world.", "Marc Andreessen"),
    ],
    "iron man": [
        ("I am Iron Man.", "Tony Stark"),
        ("Sometimes you gotta run before you can walk.", "Tony Stark"),
        ("Genius, billionaire, playboy, philanthropist. You know, the usual.", "Tony Stark"),
        ("Part of the journey is the end.", "Tony Stark"),
        ("No amount of money ever bought a second of time.", "Tony Stark"),
        ("Everybody wants a happy ending, right? But it doesn't always roll that way.", "Tony Stark"),
    ],
}


def get_quote(category: str = "") -> str:
    if category:
        cat_lower = category.lower()
        for key in _QUOTES:
            if cat_lower in key or key in cat_lower:
                quote, author = random.choice(_QUOTES[key])
                return f'"{quote}" — {author}.'

    # Daily deterministic quote
    all_quotes = [q for quotes in _QUOTES.values() for q in quotes]
    idx        = date.today().toordinal() % len(all_quotes)
    quote, author = all_quotes[idx]
    return f'Daily quote, sir: "{quote}" — {author}.'


def get_random_quote() -> str:
    all_quotes = [q for quotes in _QUOTES.values() for q in quotes]
    quote, author = random.choice(all_quotes)
    return f'"{quote}" — {author}.'


def list_categories() -> str:
    return f"Quote categories: {', '.join(_QUOTES.keys())}, sir."
