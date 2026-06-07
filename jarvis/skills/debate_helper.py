"""
jarvis/skills/debate_helper.py
Debate helper — JARVIS presents both sides of any topic
and helps you form arguments using the Socratic method.
"""
import random

_TOPICS = {
    "ai": {
        "for":     ["AI increases productivity and eliminates repetitive tasks",
                    "AI can solve complex problems faster than humans",
                    "AI democratises access to expertise for everyone"],
        "against": ["AI threatens jobs across multiple industries",
                    "AI systems can perpetuate and amplify human biases",
                    "Unchecked AI development poses existential risks"],
    },
    "remote work": {
        "for":     ["Remote work improves work-life balance significantly",
                    "Companies save on office costs and attract global talent",
                    "Productivity studies show remote workers are often more effective"],
        "against": ["Remote work isolates employees and reduces collaboration",
                    "Home environments have more distractions than offices",
                    "Career growth is slower without face-to-face visibility"],
    },
    "social media": {
        "for":     ["Social media connects billions and spreads information instantly",
                    "It gives marginalised voices a global platform",
                    "It drives commerce and entrepreneurship at scale"],
        "against": ["Social media is linked to anxiety, depression and loneliness",
                    "It spreads misinformation faster than corrections can follow",
                    "Algorithm-driven content creates dangerous echo chambers"],
    },
    "cryptocurrency": {
        "for":     ["Crypto enables financial access for the unbanked",
                    "Decentralisation removes reliance on corrupt institutions",
                    "Blockchain technology has applications far beyond currency"],
        "against": ["Crypto is highly volatile and unsuitable as a currency",
                    "It consumes enormous amounts of energy",
                    "It facilitates money laundering and illegal activity"],
    },
}


def get_both_sides(topic: str) -> str:
    topic_lower = topic.lower()
    data        = None
    for key in _TOPICS:
        if topic_lower in key or key in topic_lower:
            data = _TOPICS[key]
            break
    if not data:
        return (
            f"I don't have a structured debate for '{topic}', sir. "
            f"Available topics: {', '.join(_TOPICS.keys())}."
        )
    for_pts    = "; ".join(data["for"][:2])
    against_pts = "; ".join(data["against"][:2])
    return (
        f"Both sides on '{topic}', sir. "
        f"FOR: {for_pts}. "
        f"AGAINST: {against_pts}."
    )


def get_argument(topic: str, side: str = "for") -> str:
    topic_lower = topic.lower()
    for key, data in _TOPICS.items():
        if topic_lower in key or key in topic_lower:
            pts = data.get(side.lower(), data["for"])
            return f"Argument {side} '{topic}', sir: {random.choice(pts)}"
    return f"Topic '{topic}' not found, sir."


def socratic_question(topic: str) -> str:
    questions = [
        f"What evidence would change your mind about {topic}?",
        f"Who benefits most from the current state of {topic}?",
        f"What assumptions are you making about {topic}?",
        f"If {topic} went in the opposite direction, what would happen?",
        f"What would someone who disagrees with you say about {topic}?",
    ]
    return f"Socratic question, sir: {random.choice(questions)}"


def list_topics() -> str:
    return f"Debate topics available: {', '.join(_TOPICS.keys())}, sir."
