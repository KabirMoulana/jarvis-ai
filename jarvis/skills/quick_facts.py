"""
jarvis/skills/quick_facts.py
Quick facts — JARVIS instantly answers common knowledge
questions without needing the LLM or internet.
"""

_FACTS = {
    "capital of france":       "Paris is the capital of France, sir.",
    "capital of usa":          "Washington D.C. is the capital of the United States, sir.",
    "capital of uk":           "London is the capital of the United Kingdom, sir.",
    "capital of japan":        "Tokyo is the capital of Japan, sir.",
    "capital of china":        "Beijing is the capital of China, sir.",
    "capital of india":        "New Delhi is the capital of India, sir.",
    "capital of australia":    "Canberra is the capital of Australia, sir.",
    "speed of light":          "The speed of light is approximately 299,792,458 metres per second, sir.",
    "speed of sound":          "The speed of sound is approximately 343 metres per second in air, sir.",
    "distance to moon":        "The Moon is approximately 384,400 kilometres from Earth, sir.",
    "distance to sun":         "The Sun is approximately 149.6 million kilometres from Earth, sir.",
    "age of universe":         "The universe is approximately 13.8 billion years old, sir.",
    "age of earth":            "The Earth is approximately 4.5 billion years old, sir.",
    "population of earth":     "Earth's population is approximately 8 billion people, sir.",
    "boiling point of water":  "Water boils at 100°C (212°F) at sea level, sir.",
    "freezing point of water": "Water freezes at 0°C (32°F), sir.",
    "pi":                      "Pi is approximately 3.14159265358979, sir.",
    "golden ratio":            "The golden ratio is approximately 1.61803398874989, sir.",
    "number of planets":       "There are 8 planets in our solar system, sir.",
    "largest planet":          "Jupiter is the largest planet in our solar system, sir.",
    "smallest planet":         "Mercury is the smallest planet in our solar system, sir.",
    "tallest mountain":        "Mount Everest is the tallest mountain at 8,849 metres, sir.",
    "deepest ocean":           "The Mariana Trench is the deepest point at approximately 11 kilometres, sir.",
    "longest river":           "The Nile is traditionally considered the longest river at 6,650 km, sir.",
    "largest ocean":           "The Pacific Ocean is the largest ocean, covering about 165 million km², sir.",
    "number of bones in human body": "The adult human body has 206 bones, sir.",
    "human heart rate":        "A normal resting heart rate is 60–100 beats per minute, sir.",
    "dna bases":               "DNA has four bases: adenine, thymine, cytosine, and guanine, sir.",
    "layers of earth":         "Earth has 4 main layers: crust, mantle, outer core, and inner core, sir.",
}


def answer(question: str) -> str | None:
    """Answer a quick knowledge question if available."""
    q_lower = question.lower().strip()
    q_lower = q_lower.replace("what is", "").replace("what's", "").replace("?", "").strip()

    for key, answer in _FACTS.items():
        if key in q_lower or q_lower in key:
            return answer
    return None


def list_topics() -> str:
    topics = list(set(k.split()[0] for k in _FACTS.keys()))[:10]
    return f"Quick facts available on: {', '.join(topics)} and more, sir."


def get_random_fact() -> str:
    import random
    return random.choice(list(_FACTS.values()))
