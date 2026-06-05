"""
jarvis/skills/smart_suggestions.py
Smart suggestions — JARVIS proactively suggests actions
based on time of day, recent activity, and context.
The closest thing to a truly proactive AI assistant.
"""
from datetime import datetime, date
import os


def get_proactive_suggestion() -> str:
    """Return a context-aware suggestion based on time and day."""
    now   = datetime.now()
    hour  = now.hour
    day   = now.weekday()  # 0=Monday, 6=Sunday
    month = now.month

    suggestions = []

    # Time-based suggestions
    if 6 <= hour < 8:
        suggestions.append("Good morning. Shall I run your daily briefing?")
    elif hour == 9:
        suggestions.append("It's 9am. A good time to check your emails and plan the day.")
    elif 12 <= hour < 13:
        suggestions.append("It's lunchtime. Stay hydrated — have you logged your water today?")
    elif hour == 14:
        suggestions.append("Post-lunch dip incoming. A Pomodoro session might help your focus.")
    elif hour == 17:
        suggestions.append("End of the workday. How about an end-of-day review?")
    elif 21 <= hour < 23:
        suggestions.append("Getting late. Your sleep quality improves with consistent bedtimes.")
    elif hour >= 23:
        suggestions.append("Past midnight, sir. Even the best engineers need rest.")

    # Day-based suggestions
    if day == 0:  # Monday
        suggestions.append("It's Monday. A good day to set weekly goals.")
    elif day == 4:  # Friday
        suggestions.append("It's Friday. A good day to review what you accomplished this week.")
    elif day in (5, 6):  # Weekend
        suggestions.append("It's the weekend. Consider scheduling personal growth time.")

    # Month-based
    if now.day == 1:
        suggestions.append("First of the month — a great time to review last month's progress.")

    if not suggestions:
        suggestions.append("All systems nominal. How can I assist you today, sir?")

    return suggestions[0]


def suggest_based_on_activity(recent_intents: list[str]) -> str:
    """Suggest next actions based on recent commands."""
    if not recent_intents:
        return get_proactive_suggestion()

    last = recent_intents[-1] if recent_intents else ""

    follow_ups = {
        "briefing":      "Shall I also check your calendar for today?",
        "email_unread":  "Would you like me to draft a reply to any of those?",
        "vitals":        "Your system is running. Shall I start the health monitor?",
        "set_timer":     "Timer set. Would you like to activate focus mode while you wait?",
        "news":          "Want me to summarise the top story in more detail?",
        "weather":       "Shall I check the UV index and plan your outdoor activity?",
        "crypto_price":  "Want me to check your portfolio performance?",
        "web_search":    "Want me to summarise the top result?",
    }
    return follow_ups.get(last, get_proactive_suggestion())


def get_daily_challenge() -> str:
    """Return a daily challenge to keep JARVIS users sharp."""
    from datetime import date
    challenges = [
        "Today's challenge: Learn one new keyboard shortcut you don't currently use.",
        "Today's challenge: Write down 3 things you want to accomplish before tonight.",
        "Today's challenge: Take a 10-minute walk without your phone.",
        "Today's challenge: Read one article outside your usual interests.",
        "Today's challenge: Do 20 push-ups before your next meal.",
        "Today's challenge: Reach out to someone you haven't spoken to in a month.",
        "Today's challenge: Spend 25 focused minutes on your most important task.",
    ]
    idx = date.today().toordinal() % len(challenges)
    return challenges[idx] + " — JARVIS."
