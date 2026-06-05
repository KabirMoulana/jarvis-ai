"""
jarvis/skills/mental_health.py
Mental wellness — JARVIS checks in on your wellbeing,
provides coping strategies, and tracks mood over time.
"""
import json
import os
import random
from datetime import date, datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "mood_log.json")

_COPING = {
    "anxious": [
        "Try box breathing: inhale 4 seconds, hold 4, exhale 4, hold 4. Repeat 4 times, sir.",
        "Name 5 things you can see, 4 you can touch, 3 you can hear. Grounding technique, sir.",
        "Write down your worries. Getting them out of your head often reduces their power, sir.",
    ],
    "stressed": [
        "Take a 10-minute walk. Physical movement reduces cortisol significantly, sir.",
        "Break your workload into the single next action. One step at a time, sir.",
        "Progressive muscle relaxation — tense and release each muscle group, sir.",
    ],
    "sad": [
        "Reach out to someone you trust. Connection is a powerful mood lifter, sir.",
        "Do one small kind thing for yourself today. You deserve care too, sir.",
        "Remember: emotions are temporary states, not permanent conditions, sir.",
    ],
    "angry": [
        "Take 3 slow deep breaths before responding to anything, sir.",
        "Physical exercise — even 10 minutes — can significantly reduce anger, sir.",
        "Write down what you're feeling without filtering. Then decide what to do with it, sir.",
    ],
    "unmotivated": [
        "Start with the 2-minute rule: if it takes less than 2 minutes, do it now, sir.",
        "Motivation follows action, not the other way around. Start anyway, sir.",
        "Break the task into the smallest possible first step, sir.",
    ],
}

_AFFIRMATIONS = [
    "You are capable of more than you think, sir.",
    "Progress, not perfection, sir.",
    "Every expert was once a beginner, sir.",
    "Your struggles do not define you. Your response to them does, sir.",
    "Rest is not weakness — it is maintenance, sir.",
]


def log_mood(mood: str, score: int = 5, note: str = "") -> str:
    """Log a mood entry. score 1-10."""
    try:
        data = []
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                data = json.load(f)
    except Exception:
        data = []

    score = max(1, min(10, score))
    entry = {
        "date":  datetime.now().isoformat(),
        "mood":  mood.lower(),
        "score": score,
        "note":  note,
    }
    data.append(entry)
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

    tip = get_coping_strategy(mood)
    return f"Mood logged: {mood} ({score}/10), sir. {tip}"


def get_coping_strategy(mood: str) -> str:
    """Get a coping strategy for a mood."""
    mood_lower = mood.lower()
    for key, strategies in _COPING.items():
        if key in mood_lower or mood_lower in key:
            return random.choice(strategies)
    return random.choice(_AFFIRMATIONS)


def get_mood_trend() -> str:
    """Analyse mood trend over the past week."""
    try:
        if not os.path.exists(_FILE):
            return "No mood data yet, sir."
        with open(_FILE) as f:
            data = json.load(f)
        recent = data[-7:] if len(data) >= 7 else data
        if not recent:
            return "No mood entries, sir."
        avg    = sum(e["score"] for e in recent) / len(recent)
        trend  = "improving" if len(recent) > 1 and recent[-1]["score"] > recent[0]["score"] else "stable"
        return (
            f"Mood trend (last {len(recent)} entries): "
            f"average {avg:.1f}/10, {trend}, sir."
        )
    except Exception as e:
        return f"Could not load mood data: {e}"


def wellness_check_in() -> str:
    """Prompt a wellness check-in."""
    questions = [
        "How are you feeling right now, on a scale of 1 to 10?",
        "Have you had enough water today?",
        "When did you last take a proper break?",
        "Is there anything weighing on your mind?",
    ]
    return random.choice(questions) + " — JARVIS."


def crisis_resources() -> str:
    """Return mental health crisis resources."""
    return (
        "If you're struggling, please reach out for support, sir. "
        "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/ "
        "Crisis Text Line (US): Text HOME to 741741. "
        "Samaritans (UK): 116 123. "
        "You are not alone."
    )
