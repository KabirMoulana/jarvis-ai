"""
jarvis/skills/idea_generator.py
Idea generator — JARVIS sparks creativity with random
business ideas, project ideas, and innovation prompts.
"""
import random
from datetime import date

_BUSINESS_IDEAS = [
    "An AI-powered meal planner that learns your taste preferences over time.",
    "A voice-controlled home inventory system that tracks pantry items.",
    "A subscription box curated by AI based on your personality profile.",
    "A platform that matches freelancers with micro-tasks under 30 minutes.",
    "An app that converts voice meetings into structured action items automatically.",
    "A smart wardrobe assistant that suggests outfits based on weather and calendar.",
    "A neighbourhood skill-sharing platform — teach what you know, learn what you don't.",
    "An AI fitness coach that adapts workouts based on how you slept.",
    "A browser extension that summarises any article in one sentence.",
    "A platform that turns your daily journal entries into annual printed books.",
]

_PROJECT_IDEAS = [
    "Build a CLI tool that summarises your git commit history into a weekly report.",
    "Create a voice-controlled Raspberry Pi robot using Python and Ollama.",
    "Build a personal finance dashboard that reads your bank CSV exports.",
    "Create a Chrome extension that blocks distracting sites during Pomodoro sessions.",
    "Build an AI-powered code reviewer that comments on your GitHub PRs.",
    "Create a WhatsApp bot that sends daily motivational quotes.",
    "Build a local web dashboard to visualise your JARVIS interaction stats.",
    "Create an Obsidian plugin that auto-tags your notes using AI.",
    "Build a CLI tool that monitors your favourite GitHub repos for new releases.",
    "Create a desktop widget that shows live crypto prices and portfolio value.",
]

_INNOVATION_PROMPTS = [
    "What if your alarm clock adjusted wake time based on your sleep quality?",
    "How might you reduce food waste using AI prediction?",
    "What would a fully voice-controlled operating system look like?",
    "How could you make learning a new language feel like a video game?",
    "What if your car could predict traffic and suggest leaving times automatically?",
    "How might you make mental health support accessible 24/7 at zero cost?",
    "What would an AI personal trainer look like that costs nothing to run?",
    "How could you use computer vision to help visually impaired people navigate cities?",
]


def get_business_idea() -> str:
    return f"Business idea, sir: {random.choice(_BUSINESS_IDEAS)}"


def get_project_idea() -> str:
    return f"Project idea, sir: {random.choice(_PROJECT_IDEAS)}"


def get_innovation_prompt() -> str:
    return f"Innovation prompt, sir: {random.choice(_INNOVATION_PROMPTS)}"


def get_daily_idea() -> str:
    all_ideas = _BUSINESS_IDEAS + _PROJECT_IDEAS
    idx       = date.today().toordinal() % len(all_ideas)
    return f"Idea of the day, sir: {all_ideas[idx]}"


def brainstorm(topic: str, count: int = 3) -> str:
    """Generate quick brainstorm starters for a topic."""
    starters = [
        f"What if {topic} could be fully automated?",
        f"Who struggles most with {topic} and why?",
        f"How would a 10-year-old explain {topic}?",
        f"What's the opposite of the current approach to {topic}?",
        f"If {topic} cost nothing, what would change?",
        f"What would make {topic} 10x better overnight?",
    ]
    picks = random.sample(starters, min(count, len(starters)))
    return f"Brainstorm on '{topic}', sir: " + " | ".join(picks) + "."
