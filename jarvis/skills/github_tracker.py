"""
jarvis/skills/github_tracker.py
GitHub tracker — JARVIS monitors your GitHub repos,
PRs, issues, and commit activity.
Uses GitHub public API (no key for public repos).
"""
import urllib.request
import json
import os

_GH_TOKEN = os.getenv("GITHUB_TOKEN", "")
_GH_USER  = os.getenv("GITHUB_USERNAME", "KabirMoulana")
_API      = "https://api.github.com"


def _headers() -> dict:
    h = {"User-Agent": "JarvisAI/3.0", "Accept": "application/vnd.github.v3+json"}
    if _GH_TOKEN:
        h["Authorization"] = f"token {_GH_TOKEN}"
    return h


def get_repo_stats(repo: str = "jarvis-ai", user: str = "") -> str:
    user = user or _GH_USER
    try:
        url = f"{_API}/repos/{user}/{repo}"
        req = urllib.request.Request(url, headers=_headers())
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        stars  = data.get("stargazers_count", 0)
        forks  = data.get("forks_count", 0)
        issues = data.get("open_issues_count", 0)
        lang   = data.get("language", "Unknown")
        desc   = data.get("description", "No description")
        return (
            f"{user}/{repo}: ⭐ {stars} stars, {forks} forks, "
            f"{issues} open issues. Language: {lang}. {desc}, sir."
        )
    except Exception as e:
        return f"Could not fetch repo stats: {e}"


def get_recent_commits(repo: str = "jarvis-ai", user: str = "", count: int = 5) -> str:
    user = user or _GH_USER
    try:
        url = f"{_API}/repos/{user}/{repo}/commits?per_page={count}"
        req = urllib.request.Request(url, headers=_headers())
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        commits = [c["commit"]["message"].split("\n")[0][:60] for c in data]
        return f"Last {len(commits)} commits on {repo}: " + "; ".join(commits) + ", sir."
    except Exception as e:
        return f"Could not fetch commits: {e}"


def get_open_issues(repo: str = "jarvis-ai", user: str = "") -> str:
    user = user or _GH_USER
    try:
        url = f"{_API}/repos/{user}/{repo}/issues?state=open&per_page=5"
        req = urllib.request.Request(url, headers=_headers())
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        if not data:
            return f"No open issues on {repo}, sir."
        issues = [f"#{i['number']}: {i['title'][:50]}" for i in data]
        return f"Open issues on {repo}: " + "; ".join(issues) + ", sir."
    except Exception as e:
        return f"Could not fetch issues: {e}"


def get_user_repos(user: str = "") -> str:
    user = user or _GH_USER
    try:
        url = f"{_API}/users/{user}/repos?per_page=10&sort=updated"
        req = urllib.request.Request(url, headers=_headers())
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        names = [r["name"] for r in data]
        return f"{user}'s repos: " + ", ".join(names) + ", sir."
    except Exception as e:
        return f"Could not fetch repos: {e}"
