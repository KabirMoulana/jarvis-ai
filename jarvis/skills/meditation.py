"""
jarvis/skills/meditation.py
Guided meditation and breathing exercises — JARVIS guides
you through mindfulness sessions with timed prompts.
"""
import time
import threading


_SESSIONS = {
    "box breathing": {
        "description": "Box breathing — equal inhale, hold, exhale, hold.",
        "steps": [
            ("Breathe in for 4 seconds ...", 4),
            ("Hold for 4 seconds ...", 4),
            ("Breathe out for 4 seconds ...", 4),
            ("Hold for 4 seconds ...", 4),
        ],
        "rounds": 4,
    },
    "4-7-8": {
        "description": "4-7-8 breathing — calms the nervous system.",
        "steps": [
            ("Inhale for 4 seconds ...", 4),
            ("Hold for 7 seconds ...", 7),
            ("Exhale slowly for 8 seconds ...", 8),
        ],
        "rounds": 3,
    },
    "deep breathing": {
        "description": "Simple deep breathing to reduce stress.",
        "steps": [
            ("Take a slow, deep breath in ...", 5),
            ("Hold ...", 2),
            ("Slowly breathe out ...", 6),
        ],
        "rounds": 5,
    },
}

_AFFIRMATIONS = [
    "You are capable of achieving great things.",
    "Every challenge makes you stronger.",
    "Your mind is your greatest weapon.",
    "You are focused, calm, and in control.",
    "Today is full of opportunity.",
    "You have overcome harder things than this.",
    "Rest is not weakness — it is fuel.",
]


def start_breathing(technique: str = "box breathing", callback=None) -> str:
    """Start a guided breathing session."""
    tech  = technique.lower().strip()
    session = None
    for key in _SESSIONS:
        if tech in key or key in tech:
            session = _SESSIONS[key]
            break
    if not session:
        techniques = ", ".join(_SESSIONS.keys())
        return f"Technique '{technique}' not found, sir. Available: {techniques}."

    def _run():
        if callback:
            callback(session["description"])
        for round_num in range(1, session["rounds"] + 1):
            if callback:
                callback(f"Round {round_num} of {session['rounds']}.")
            for prompt, duration in session["steps"]:
                print(f"\n🧘  {prompt}")
                if callback:
                    callback(prompt)
                time.sleep(duration)
        msg = "Breathing exercise complete, sir. How do you feel?"
        print(f"\n✓  {msg}")
        if callback:
            callback(msg)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return f"Starting {technique}, sir. {session['rounds']} rounds."


def get_affirmation() -> str:
    """Return a random daily affirmation."""
    import random
    return random.choice(_AFFIRMATIONS) + " — JARVIS."


def quick_mindfulness(callback=None) -> str:
    """One-minute mindfulness check-in."""
    def _run():
        prompts = [
            "Close your eyes if you can, sir.",
            "Notice your breath. Don't change it — just observe.",
            "Scan your body from head to toe. Release any tension.",
            "Focus on this moment. Nothing else exists right now.",
            "Take one deep breath. In through the nose, out through the mouth.",
            "You are present. You are focused. Open your eyes when ready.",
        ]
        for i, p in enumerate(prompts):
            if callback:
                callback(p)
            else:
                print(f"\n🧘  {p}")
            time.sleep(10)
        if callback:
            callback("Mindfulness check-in complete, sir.")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return "Starting one-minute mindfulness session, sir."
