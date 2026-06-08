"""
jarvis/skills/voice_commands_v2.py
Extended voice command patterns — adds 50+ new intent
patterns for all Day 5/6/7 skills to the command router.
"""
import re
from datetime import datetime

# Extended patterns for new Day 5/6/7 skills
EXTENDED_PATTERNS = [
    # Goals
    (r"\badd\s+goal\b",                          "add_goal"),
    (r"\bmy\s+goals?\b",                         "list_goals"),
    (r"\bgoal\s+progress\b",                     "goal_stats"),
    (r"\bupdate\s+goal\b",                       "update_goal"),

    # 2FA
    (r"\b2fa\s+code\s+for\s+(.+)\b",            "get_2fa"),
    (r"\btotp\s+(.+)\b",                         "get_2fa"),
    (r"\btwo\s+factor\s+(.+)\b",                 "get_2fa"),

    # Ambient sounds
    (r"\bplay\s+(.+)\s+sounds?\b",               "ambient_sound"),
    (r"\bambient\s+(.+)\b",                      "ambient_sound"),
    (r"\bsounds?\s+for\s+(.+)\b",               "ambient_mood"),

    # Events
    (r"\bcreate\s+(?:an?\s+)?event\b",           "create_event"),
    (r"\bevent\s+checklist\b",                   "event_checklist"),
    (r"\bdays?\s+until\s+(.+)\b",               "days_until"),

    # Meal planning
    (r"\b(?:generate|create|make)\s+meal\s+plan\b",  "meal_plan"),
    (r"\btoday'?s?\s+meals?\b",                  "todays_meals"),
    (r"\bwhat(?:'s| is)\s+for\s+(breakfast|lunch|dinner)\b", "suggest_meal"),

    # Challenges
    (r"\bstart\s+(?:the\s+)?(.+)\s+challenge\b", "start_challenge"),
    (r"\btoday'?s?\s+challenge\s+task\b",        "challenge_task"),
    (r"\bcomplete\s+(?:today'?s?\s+)?challenge\b","complete_challenge"),

    # Backup
    (r"\bbackup\s+(?:jarvis\s+)?memory\b",       "backup_memory"),
    (r"\blist\s+backups?\b",                     "list_backups"),

    # Password vault
    (r"\bget\s+password\s+for\s+(.+)\b",         "get_password"),
    (r"\bsave\s+password\s+for\s+(.+)\b",        "save_password"),
    (r"\blist\s+(?:saved\s+)?passwords?\b",      "list_passwords"),

    # Productivity report
    (r"\bweekly\s+report\b",                     "weekly_report"),
    (r"\bproductivity\s+report\b",               "weekly_report"),
    (r"\bstreak\s+summary\b",                    "streak_summary"),

    # Quick facts
    (r"\bwhat\s+is\s+the\s+capital\s+of\s+(.+)\b", "quick_fact"),
    (r"\bspeed\s+of\s+(light|sound)\b",          "quick_fact"),
    (r"\brandom\s+fact\b",                       "random_fact"),

    # Ideas
    (r"\bgive\s+me\s+(?:a\s+)?(?:business|startup)\s+idea\b", "business_idea"),
    (r"\bproject\s+idea\b",                      "project_idea"),
    (r"\binnovation\s+prompt\b",                 "innovation_prompt"),
    (r"\bbrainstorm\s+(.+)\b",                   "brainstorm"),
    (r"\bidea\s+of\s+the\s+day\b",              "daily_idea"),

    # Relationship tracker
    (r"\bcheck\s+in\s+with\s+(.+)\b",           "relationship_checkin"),
    (r"\boverdue\s+(?:contact|relationship)s?\b","overdue_contacts"),
    (r"\badd\s+(?:person|contact)\s+(.+)\b",    "add_person"),

    # Debate
    (r"\bboth\s+sides\s+of\s+(.+)\b",           "both_sides"),
    (r"\bargue\s+(for|against)\s+(.+)\b",        "get_argument"),
    (r"\bsocratic\s+question\s+(?:about\s+)?(.+)\b", "socratic_q"),

    # Carbon footprint
    (r"\bcarbon\s+footprint\b",                  "carbon_tips"),
    (r"\bco2\s+(?:for\s+)?(?:my\s+)?flight\b",  "flight_carbon"),

    # Sleep
    (r"\blog\s+(?:my\s+)?sleep\b",              "log_sleep"),
    (r"\bsleep\s+(?:quality|stats|trend)\b",    "sleep_stats"),
    (r"\bsleep\s+calculator\b",                 "sleep_calc"),

    # GitHub
    (r"\bgithub\s+(?:repo\s+)?stats\b",         "github_stats"),
    (r"\brecent\s+commits\b",                   "recent_commits"),
    (r"\bopen\s+issues\b",                      "open_issues"),
]

_COMPILED_V2 = [(re.compile(p, re.IGNORECASE), label) for p, label in EXTENDED_PATTERNS]


def route_extended(command: str) -> dict | None:
    """Check extended patterns. Returns intent dict or None."""
    for pattern, label in _COMPILED_V2:
        m = pattern.search(command)
        if m:
            args = [g for g in m.groups() if g is not None]
            return {"intent": label, "args": args, "raw": command}
    return None
