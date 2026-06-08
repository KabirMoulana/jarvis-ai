"""
jarvis/skills/productivity_report.py
Productivity report — JARVIS compiles a weekly/monthly
productivity summary from all tracked data.
"""
import json
import os
from datetime import date, timedelta


def generate_weekly_report() -> str:
    """Generate a comprehensive weekly productivity report."""
    sections = [f"Weekly productivity report — week of {date.today().strftime('%B %d, %Y')}, sir."]

    # Tasks completed
    try:
        todo_file = os.path.join(os.path.dirname(__file__), "..", "memory", "todos.json")
        if os.path.exists(todo_file):
            with open(todo_file) as f:
                todos = json.load(f)
            week_ago  = str(date.today() - timedelta(days=7))
            completed = [t for t in todos if t.get("done") and
                        (t.get("completed", "") or "") >= week_ago]
            sections.append(f"Tasks completed: {len(completed)}.")
    except Exception:
        pass

    # Habits tracked
    try:
        habits_file = os.path.join(os.path.dirname(__file__), "..", "memory", "habits.json")
        if os.path.exists(habits_file):
            with open(habits_file) as f:
                habits = json.load(f)
            today     = date.today()
            week_logs = []
            for habit_data in habits.values():
                logs = habit_data.get("log", [])
                week_logs.extend([l for l in logs
                                  if l >= str(today - timedelta(days=7))])
            sections.append(f"Habit check-ins this week: {len(week_logs)}.")
    except Exception:
        pass

    # Study time
    try:
        study_file = os.path.join(os.path.dirname(__file__), "..", "memory", "study_log.json")
        if os.path.exists(study_file):
            with open(study_file) as f:
                study = json.load(f)
            week_ago   = str(date.today() - timedelta(days=7))
            week_mins  = sum(
                mins for day, subjects in study.items()
                if day >= week_ago
                for mins in subjects.values()
            )
            sections.append(f"Study time: {week_mins} minutes ({week_mins/60:.1f} hours).")
    except Exception:
        pass

    # Workouts
    try:
        workout_file = os.path.join(os.path.dirname(__file__), "..", "memory", "workouts.json")
        if os.path.exists(workout_file):
            with open(workout_file) as f:
                workouts = json.load(f)
            week_ago    = str(date.today() - timedelta(days=7))
            this_week   = [w for w in workouts if w.get("date", "") >= week_ago]
            sections.append(f"Workouts logged: {len(this_week)}.")
    except Exception:
        pass

    # Pomodoros
    try:
        pomo_file = os.path.join(os.path.dirname(__file__), "..", "memory", "pomodoro.json")
        if os.path.exists(pomo_file):
            with open(pomo_file) as f:
                pomo = json.load(f)
            week_ago = str(date.today() - timedelta(days=7))
            total    = sum(v for k, v in pomo.items() if k >= week_ago)
            sections.append(f"Pomodoro sessions: {total} ({total * 25} minutes of focused work).")
    except Exception:
        pass

    if len(sections) == 1:
        sections.append("No detailed tracking data found. Start logging habits, tasks and workouts for richer reports.")

    return " ".join(sections)


def get_streak_summary() -> str:
    """Summary of all current streaks."""
    streaks = []

    try:
        from jarvis.skills.habit_tracker import get_habits_summary
        streaks.append(get_habits_summary())
    except Exception:
        pass

    try:
        from jarvis.skills.workout_tracker import get_workout_streak
        streaks.append(get_workout_streak())
    except Exception:
        pass

    if not streaks:
        return "No streak data available, sir."
    return "Streak summary, sir: " + " | ".join(streaks)
