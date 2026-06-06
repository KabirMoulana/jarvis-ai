"""
jarvis/skills/life_tips.py
Life tips and hacks — JARVIS shares practical wisdom
across productivity, health, finance, and general life advice.
"""
import random
from datetime import date

_TIPS = {
    "productivity": [
        "Eat the frog first — do your most dreaded task before anything else, sir.",
        "The two-minute rule: if it takes less than two minutes, do it now.",
        "Single-tasking beats multitasking. Focus is a superpower, sir.",
        "Schedule your most important work during your peak energy hours, sir.",
        "Batch similar tasks together to reduce context switching, sir.",
        "A done imperfect is better than a perfect undone, sir.",
        "Your environment shapes your behaviour. Design it for the outcomes you want, sir.",
    ],
    "health": [
        "The best workout is the one you'll actually do consistently, sir.",
        "Drink a glass of water before every meal. It aids digestion and reduces overeating, sir.",
        "Standing for 10 minutes every hour reduces sedentary risk significantly, sir.",
        "Sleep is the foundation — everything else builds on it, sir.",
        "Sunlight in the morning resets your circadian rhythm and improves mood, sir.",
        "Chew your food slowly — it improves digestion and reduces overeating, sir.",
    ],
    "finance": [
        "Pay yourself first — automate savings before spending, sir.",
        "The latte factor is real — small daily expenses compound into thousands yearly, sir.",
        "An emergency fund of 3-6 months expenses changes your risk tolerance entirely, sir.",
        "Invest consistently over time rather than trying to time the market, sir.",
        "Track your net worth monthly — what gets measured gets managed, sir.",
        "Never make major financial decisions when emotional, sir.",
    ],
    "relationships": [
        "Listen to understand, not to respond. Most people just want to be heard, sir.",
        "Express gratitude specifically — 'thank you for X' means more than 'thanks', sir.",
        "Assume positive intent. Most conflicts stem from miscommunication, not malice, sir.",
        "Invest in relationships before you need them. Networks built in need feel transactional, sir.",
        "Be the kind of friend you want to have, sir.",
    ],
    "mindset": [
        "Your beliefs about your abilities shape your outcomes more than your actual abilities, sir.",
        "Comparison is the thief of joy. Compete with yesterday's version of yourself, sir.",
        "Failure is data, not identity. Extract the lesson and iterate, sir.",
        "Comfort is the enemy of growth. Do something uncomfortable every day, sir.",
        "What you resist, persists. Face challenges directly rather than avoiding them, sir.",
    ],
}


def get_tip(category: str = "") -> str:
    """Return a life tip, optionally from a specific category."""
    if category:
        for key in _TIPS:
            if category.lower() in key or key in category.lower():
                return random.choice(_TIPS[key]) + " — JARVIS."
    all_tips = [t for tips in _TIPS.values() for t in tips]
    return random.choice(all_tips) + " — JARVIS."


def get_daily_tip() -> str:
    """Return a consistent daily tip."""
    all_tips = [t for tips in _TIPS.values() for t in tips]
    idx      = date.today().toordinal() % len(all_tips)
    return all_tips[idx] + " — JARVIS."


def list_categories() -> str:
    return f"Life tip categories: {', '.join(_TIPS.keys())}, sir."
