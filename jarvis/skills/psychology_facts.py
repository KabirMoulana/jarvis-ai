"""Psychology facts — JARVIS explains psychological phenomena and biases."""
import random

_BIASES = {
    "confirmation bias": "The tendency to search for information that confirms existing beliefs, sir.",
    "dunning-kruger": "Low-skill individuals overestimate their ability; experts underestimate theirs, sir.",
    "sunk cost fallacy": "Continuing because of past investment, even when it's no longer rational, sir.",
    "anchoring bias": "Over-relying on the first piece of information encountered, sir.",
    "availability heuristic": "Judging probability based on how easily examples come to mind, sir.",
    "halo effect": "Letting one positive trait influence your overall judgement of a person, sir.",
    "bystander effect": "People less likely to help when others are present — diffusion of responsibility, sir.",
    "recency bias": "Giving more weight to recent events than older ones, sir.",
    "loss aversion": "Losses feel twice as painful as equivalent gains feel good, sir.",
    "cognitive dissonance": "Mental discomfort from holding contradictory beliefs simultaneously, sir.",
}

_FACTS = [
    "It takes approximately 66 days to form a new habit, not 21 as commonly believed, sir.",
    "The human brain can store approximately 2.5 petabytes of information, sir.",
    "Decision fatigue is real — willpower depletes throughout the day, sir.",
    "Multitasking reduces productivity by up to 40% — the brain switches tasks, not multitasks, sir.",
    "Social connection is as important to health as diet and exercise, sir.",
    "Writing things down improves memory retention by up to 33%, sir.",
    "The brain cannot distinguish between real and vividly imagined experiences, sir.",
    "Stress shrinks the hippocampus — the brain region responsible for memory, sir.",
]

def get_bias(name: str) -> str:
    for key, desc in _BIASES.items():
        if key in name.lower() or name.lower() in key:
            return f"{key.title()}: {desc}"
    return f"Bias not found. Available: {', '.join(_BIASES.keys())}, sir."

def get_fact() -> str:
    return random.choice(_FACTS)

def list_biases() -> str:
    return f"Cognitive biases: {', '.join(_BIASES.keys())}, sir."
