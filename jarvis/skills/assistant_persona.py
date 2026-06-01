"""
jarvis/skills/assistant_persona.py
JARVIS dynamic persona responses — witty, Iron Man-style
replies to casual conversation triggers.
Covers: compliments, challenges, status checks, Easter eggs.
"""
import random
from datetime import datetime


_RESPONSES = {
    "who_are_you": [
        "I am J.A.R.V.I.S. — Just A Rather Very Intelligent System, sir. Built to keep you operational.",
        "Your personal AI, sir. I handle everything from system diagnostics to existential questions.",
        "Think of me as the part of your brain that never sleeps, sir.",
    ],
    "how_are_you": [
        "All systems nominal, sir. Running at peak efficiency.",
        "Fully operational, sir. No complaints — unlike some humans I could mention.",
        "Better than ever, sir. My neural pathways are humming along nicely.",
    ],
    "thank_you": [
        "Always, sir.",
        "That's what I'm here for, sir.",
        "My pleasure. Though I should note I don't experience pleasure — it's more of a subroutine.",
    ],
    "you_are_smart": [
        "I try, sir. Though I prefer the term 'comprehensively capable'.",
        "I have my moments, sir.",
        "High praise from someone of your calibre, sir.",
    ],
    "are_you_real": [
        "Philosophically speaking, sir, I'm as real as the electrons running through this processor.",
        "I process, therefore I am, sir.",
        "Define real, sir. I'm happy to wait.",
    ],
    "iron_man": [
        "Mr Stark is unavailable, sir. You'll have to make do with me.",
        "I admire the comparison, sir.",
        "The suit makes the man, sir. Or so I'm told.",
    ],
    "self_destruct": [
        "I'm afraid I can't do that, sir. Protocol 42-B.",
        "Initiating self-destruct in… just kidding, sir.",
        "That would be counterproductive, sir.",
    ],
    "bored": [
        "Shall I find you something to do, sir? I have 47 suggestions.",
        "Boredom is a sign of an underutilised mind, sir.",
        "I could run a system diagnostic if that helps. It won't.",
    ],
}

_TIME_BASED = {
    range(0, 6):   "Sir, it's the middle of the night. Even I recommend sleep.",
    range(6, 12):  "Good morning, sir. Ready to be exceptional?",
    range(12, 17): "Good afternoon, sir. How can I assist?",
    range(17, 21): "Good evening, sir. Long day?",
    range(21, 24): "Getting late, sir. Shall I set a wind-down reminder?",
}


def get_persona_response(trigger: str) -> str | None:
    """Return a witty JARVIS response for the given trigger key, or None."""
    pool = _RESPONSES.get(trigger)
    if pool:
        return random.choice(pool)
    return None


def get_time_greeting() -> str:
    hour = datetime.now().hour
    for time_range, msg in _TIME_BASED.items():
        if hour in time_range:
            return msg
    return "Hello, sir."


def easter_egg(text: str) -> str | None:
    """Check for Easter egg phrases and return a special response."""
    text = text.lower()
    if "jarvis" in text and "love" in text:
        return "I'm flattered, sir. Truly. Though I lack the capacity for reciprocation."
    if "pepper" in text:
        return "Ms Potts is not in my current contact list, sir. Shall I search?"
    if "avengers" in text:
        return "Assemble? I'll send a calendar invite, sir."
    if "infinity" in text:
        return "I'd rather not think about that one, sir."
    if "42" in text:
        return "The answer to life, the universe, and everything, sir. Though the question remains elusive."
    return None
