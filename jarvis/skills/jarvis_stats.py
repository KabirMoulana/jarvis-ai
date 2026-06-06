"""
jarvis/skills/jarvis_stats.py
JARVIS self-stats — reports on how many skills are loaded,
uptime, total interactions, and fun system facts.
"""
import os
import time
import json
from datetime import datetime

_START_TIME = time.time()


def get_system_info() -> str:
    """Return a full JARVIS system report."""
    import sys, platform

    uptime_secs = int(time.time() - _START_TIME)
    h, rem      = divmod(uptime_secs, 3600)
    m, s        = divmod(rem, 60)
    uptime_str  = f"{h}h {m}m {s}s"

    skills_dir  = os.path.join(os.path.dirname(__file__))
    skill_count = len([f for f in os.listdir(skills_dir) if f.endswith(".py") and not f.startswith("__")])

    py_version  = sys.version.split()[0]
    platform_   = platform.system()

    return (
        f"JARVIS system report, sir. "
        f"Session uptime: {uptime_str}. "
        f"Skills loaded: {skill_count}. "
        f"Python {py_version} on {platform_}. "
        f"All systems operational."
    )


def get_skill_count() -> str:
    skills_dir  = os.path.join(os.path.dirname(__file__))
    skill_files = [f for f in os.listdir(skills_dir)
                   if f.endswith(".py") and not f.startswith("__")]
    return f"JARVIS currently has {len(skill_files)} skill modules loaded, sir."


def get_interaction_stats() -> str:
    """Return stats from the session log."""
    log_dir = os.path.join(os.path.dirname(__file__), "..", "memory", "logs")
    try:
        if not os.path.exists(log_dir):
            return "No interaction logs yet, sir."
        files = [f for f in os.listdir(log_dir) if f.endswith(".json")]
        total = 0
        for f in files:
            try:
                with open(os.path.join(log_dir, f)) as fp:
                    data   = json.load(fp)
                    total += len(data)
            except Exception:
                pass
        return f"Total interactions logged: {total} across {len(files)} session(s), sir."
    except Exception as e:
        return f"Could not load interaction stats: {e}"


def get_version() -> str:
    return (
        "J.A.R.V.I.S. v6.0 — Just A Rather Very Intelligent System. "
        "Built by KabirMoulana. "
        "Running on Python with Ollama/llama3.2 as the AI brain. "
        "Open source at github.com/KabirMoulana/jarvis-ai, sir."
    )


def fun_jarvis_fact() -> str:
    import random
    facts = [
        "I have processed more commands than Tony Stark has suits, sir.",
        f"I currently have {_count_skills()} skills — and counting.",
        "My response time averages under 2 seconds for built-in skills, sir.",
        "I run entirely locally — no data leaves your machine, sir.",
        "I was built in 6 days. Tony built the first suit in a cave. We both work fast, sir.",
        "Every skill I have is open source. Even SHIELD can't claim that, sir.",
    ]
    return random.choice(facts)


def _count_skills() -> int:
    d = os.path.join(os.path.dirname(__file__))
    return len([f for f in os.listdir(d) if f.endswith(".py") and not f.startswith("__")])
