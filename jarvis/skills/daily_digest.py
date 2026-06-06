"""
jarvis/skills/daily_digest.py
Daily digest — JARVIS compiles a comprehensive morning briefing
combining news, weather, calendar, tasks, health, and motivation.
The ultimate Iron Man morning report.
"""
from datetime import datetime, date


def get_full_digest(location: str = "", callback=None) -> str:
    """
    Compile a full daily digest from all available skills.
    Returns a formatted multi-section briefing.
    """
    now      = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    sections = []

    # ── Greeting ──────────────────────────────────────────────────────────────
    hour = now.hour
    if hour < 12:   greeting = "Good morning"
    elif hour < 17: greeting = "Good afternoon"
    else:           greeting = "Good evening"
    sections.append(f"{greeting}, sir. It is {time_str} on {date_str}.")

    # ── Weather ───────────────────────────────────────────────────────────────
    if location:
        try:
            from jarvis.skills.web_skills import get_weather
            sections.append(get_weather(location))
        except Exception:
            pass

    # ── System vitals ─────────────────────────────────────────────────────────
    try:
        from jarvis.skills.vitals import get_vitals
        sections.append(get_vitals())
    except Exception:
        pass

    # ── Calendar ──────────────────────────────────────────────────────────────
    try:
        from jarvis.skills.calendar_skill import get_today_events
        sections.append(get_today_events())
    except Exception:
        pass

    # ── To-do ─────────────────────────────────────────────────────────────────
    try:
        from jarvis.skills.todo import list_tasks
        sections.append(list_tasks())
    except Exception:
        pass

    # ── Top news ──────────────────────────────────────────────────────────────
    try:
        from jarvis.skills.news_summarizer import get_briefing_headlines
        sections.append(get_briefing_headlines())
    except Exception:
        pass

    # ── Health ────────────────────────────────────────────────────────────────
    try:
        from jarvis.skills.health_tracker import daily_health_summary
        sections.append(daily_health_summary())
    except Exception:
        pass

    # ── Motivation ────────────────────────────────────────────────────────────
    try:
        from jarvis.skills.quote_of_day import get_quote
        sections.append(get_quote("morning"))
    except Exception:
        pass

    # ── Birthday check ────────────────────────────────────────────────────────
    try:
        from jarvis.skills.birthday_tracker import check_today_birthdays
        bday = check_today_birthdays()
        if bday:
            sections.append(bday)
    except Exception:
        pass

    # ── Daily challenge ───────────────────────────────────────────────────────
    try:
        from jarvis.skills.smart_suggestions import get_daily_challenge
        sections.append(get_daily_challenge())
    except Exception:
        pass

    digest = " ".join(s for s in sections if s)
    return digest if digest else f"Good morning, sir. All systems operational at {time_str}."


def get_evening_digest(location: str = "") -> str:
    """Evening wrap-up digest."""
    now      = datetime.now()
    sections = [f"Good evening, sir. It is {now.strftime('%I:%M %p')}."]

    try:
        from jarvis.skills.daily_planner import end_of_day_review
        sections.append(end_of_day_review())
    except Exception:
        pass

    try:
        from jarvis.skills.habit_tracker import get_habits_summary
        sections.append(get_habits_summary())
    except Exception:
        pass

    try:
        from jarvis.skills.quote_of_day import get_quote
        sections.append(get_quote("stoic"))
    except Exception:
        pass

    sections.append("Rest well, sir. Tomorrow awaits.")
    return " ".join(s for s in sections if s)
