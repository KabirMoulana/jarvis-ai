"""Productivity matrix — JARVIS helps decide what to work on using various frameworks."""
import random

def energy_based_suggestion() -> str:
    from datetime import datetime
    hour = datetime.now().hour
    if 6 <= hour < 10:
        return "Peak energy window, sir. Tackle your most cognitively demanding task now — deep work, writing, or complex problem solving."
    elif 10 <= hour < 12:
        return "Still high energy, sir. Good for meetings, collaboration, and creative work."
    elif 12 <= hour < 14:
        return "Post-lunch dip incoming, sir. Ideal for admin tasks, emails, and routine work."
    elif 14 <= hour < 16:
        return "Secondary peak, sir. Good for analytical work and decision making."
    elif 16 <= hour < 18:
        return "Energy declining, sir. Wrap up tasks, plan tomorrow, review progress."
    else:
        return "Evening mode, sir. Light tasks only — reading, learning, or creative hobbies."

def mit_method(tasks: list[str]) -> str:
    """Most Important Tasks — identify the top 3."""
    if not tasks:
        return "No tasks provided, sir."
    if len(tasks) <= 3:
        return f"Your MITs (Most Important Tasks): {', '.join(tasks)}, sir."
    return (f"Choose your 3 MITs from: {', '.join(tasks)}. "
            f"Complete these before anything else, sir.")

def get_deep_work_prompt() -> str:
    prompts = [
        "Schedule a 90-minute deep work block with no interruptions, sir.",
        "Before starting, write down the ONE thing you want to accomplish this session.",
        "Put your phone in another room. Notifications are the enemy of deep work, sir.",
        "Start with the hardest part. Your future self will thank you, sir.",
        "Set a specific end time — constraints improve focus, sir.",
    ]
    return random.choice(prompts)

def time_boxing(task: str, minutes: int = 25) -> str:
    return (f"Time box set, sir: '{task}' for exactly {minutes} minutes. "
            f"Work on ONLY this. When the timer ends, stop and evaluate progress.")

def get_framework(name: str) -> str:
    frameworks = {
        "pomodoro": "25 minutes focused work, 5 minute break. After 4 rounds, take a 15-30 minute break, sir.",
        "time blocking": "Assign every hour of your day to a specific task in advance, sir.",
        "gtd": "Getting Things Done: capture everything, clarify, organise, review, engage, sir.",
        "eat the frog": "Do your most dreaded task first thing in the morning, sir.",
        "parkinson's law": "Work expands to fill the time available. Set artificial deadlines, sir.",
        "80/20": "20% of your actions produce 80% of your results. Find and focus on that 20%, sir.",
    }
    for key, desc in frameworks.items():
        if name.lower() in key or key in name.lower():
            return f"{key.title()}: {desc}"
    return f"Framework not found. Available: {', '.join(frameworks.keys())}, sir."
