"""
jarvis/skills/science_facts.py
Science facts and explanations — JARVIS explains scientific
concepts in simple terms and shares fascinating facts.
"""
import random

_CONCEPTS = {
    "black hole": (
        "A black hole is a region in space where gravity is so strong that "
        "nothing — not even light — can escape. They form when massive stars collapse. "
        "The boundary is called the event horizon, sir."
    ),
    "quantum entanglement": (
        "Quantum entanglement is when two particles become linked — measuring one "
        "instantly affects the other, regardless of distance. Einstein called it "
        "'spooky action at a distance', sir."
    ),
    "dna": (
        "DNA is the molecule that carries genetic instructions for all living organisms. "
        "It's shaped like a double helix, and if you stretched out the DNA from one "
        "human cell, it would be about 2 metres long, sir."
    ),
    "relativity": (
        "Einstein's theory of relativity says time and space are relative — they change "
        "based on speed and gravity. GPS satellites have to account for time dilation "
        "to give accurate locations, sir."
    ),
    "photosynthesis": (
        "Photosynthesis is how plants convert sunlight, water, and CO2 into glucose "
        "and oxygen. Essentially, plants eat sunlight. Without it, almost all life "
        "on Earth would cease to exist, sir."
    ),
    "gravity": (
        "Gravity is the force of attraction between masses. Einstein described it not "
        "as a force but as a curvature in spacetime caused by mass. The more massive "
        "an object, the more it warps spacetime around it, sir."
    ),
    "evolution": (
        "Evolution is the process by which species change over time through natural "
        "selection. Traits that help survival get passed on. All life on Earth shares "
        "a common ancestor, sir."
    ),
    "dark matter": (
        "Dark matter is invisible matter that doesn't interact with light but has "
        "gravitational effects. It makes up about 27% of the universe, yet we've "
        "never directly detected it, sir."
    ),
}

_FACTS = [
    "A teaspoon of neutron star material would weigh about 10 million tonnes, sir.",
    "The human body contains enough carbon to make 900 pencils, sir.",
    "Lightning strikes the Earth about 100 times every second, sir.",
    "The universe is about 13.8 billion years old, sir.",
    "There are more atoms in a glass of water than glasses of water in all the oceans, sir.",
    "Sound travels about 4 times faster in water than in air, sir.",
    "The hottest temperature ever recorded in a lab was 4 trillion degrees Celsius — in a particle collider, sir.",
    "Bananas are slightly radioactive due to their potassium-40 content, sir.",
    "A day on Venus is longer than a year on Venus, sir.",
    "Octopuses have three hearts and blue copper-based blood, sir.",
]


def explain(concept: str) -> str:
    """Explain a scientific concept."""
    concept_lower = concept.lower().strip()
    for key, explanation in _CONCEPTS.items():
        if key in concept_lower or concept_lower in key:
            return explanation
    return (
        f"I don't have a stored explanation for '{concept}', sir. "
        f"Enable Ollama for a detailed explanation."
    )


def get_fact() -> str:
    """Return a random science fact."""
    return random.choice(_FACTS)


def get_fact_by_topic(topic: str) -> str:
    """Return a fact related to a topic."""
    topic_lower = topic.lower()
    relevant    = [f for f in _FACTS if topic_lower in f.lower()]
    if relevant:
        return random.choice(relevant)
    return get_fact()


def list_concepts() -> str:
    return f"I can explain: {', '.join(_CONCEPTS.keys())}, sir."
