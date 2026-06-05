"""
jarvis/skills/startup_news.py
Tech and startup news — JARVIS fetches the latest from
Hacker News, TechCrunch RSS and Product Hunt.
"""
import urllib.request
import json
import xml.etree.ElementTree as ET
import re


_HN_API = "https://hacker-news.firebaseio.com/v0"
_TC_RSS = "https://techcrunch.com/feed/"


def get_hacker_news_top(count: int = 5) -> str:
    """Fetch top stories from Hacker News."""
    try:
        url = f"{_HN_API}/topstories.json"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            story_ids = json.loads(resp.read())[:count]

        stories = []
        for sid in story_ids:
            try:
                r = urllib.request.Request(
                    f"{_HN_API}/item/{sid}.json",
                    headers={"User-Agent": "JarvisAI/3.0"}
                )
                with urllib.request.urlopen(r, timeout=4) as resp:
                    item = json.loads(resp.read())
                title  = item.get("title", "No title")
                score  = item.get("score", 0)
                stories.append(f"{title} ({score} points)")
            except Exception:
                pass

        if not stories:
            return "Could not fetch Hacker News stories, sir."
        return f"Top Hacker News stories: " + " | ".join(stories) + ", sir."
    except Exception as e:
        return f"Hacker News unavailable: {e}"


def get_techcrunch_headlines(count: int = 4) -> str:
    """Fetch latest TechCrunch headlines."""
    try:
        req = urllib.request.Request(_TC_RSS, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            root = ET.fromstring(resp.read())
        items  = root.findall(".//item")[:count]
        titles = [i.findtext("title", "").strip() for i in items]
        return "TechCrunch: " + " | ".join(titles) + ", sir."
    except Exception as e:
        return f"TechCrunch feed unavailable: {e}"


def get_product_hunt_today() -> str:
    """Open Product Hunt for today's top products."""
    import webbrowser
    webbrowser.open("https://www.producthunt.com")
    return "Opening Product Hunt for today's top products, sir."


def get_dev_news() -> str:
    """Get headlines from dev.to RSS."""
    try:
        url = "https://dev.to/feed"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            root  = ET.fromstring(resp.read())
        items  = root.findall(".//item")[:4]
        titles = [i.findtext("title", "").strip() for i in items]
        return "Dev.to trending: " + " | ".join(titles) + ", sir."
    except Exception as e:
        return f"Dev.to unavailable: {e}"


def get_github_trending() -> str:
    """Open GitHub trending page."""
    import webbrowser
    webbrowser.open("https://github.com/trending")
    return "Opening GitHub Trending, sir."
