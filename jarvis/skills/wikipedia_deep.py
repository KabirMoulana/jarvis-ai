"""
jarvis/skills/wikipedia_deep.py
Deep Wikipedia integration — JARVIS fetches full article
summaries, related topics, and on-this-day facts.
"""
import urllib.request
import urllib.parse
import json
from datetime import date


_API = "https://en.wikipedia.org/api/rest_v1"
_SEARCH = "https://en.wikipedia.org/w/api.php"


def get_summary(topic: str) -> str:
    """Get a concise Wikipedia summary."""
    try:
        encoded = urllib.parse.quote(topic.replace(" ", "_"))
        url     = f"{_API}/page/summary/{encoded}"
        req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data    = json.loads(resp.read())
        title   = data.get("title", topic)
        extract = data.get("extract", "No summary available.")
        # Trim to 3 sentences
        sentences = extract.split(". ")
        summary   = ". ".join(sentences[:3]) + "."
        return f"{title}: {summary}, sir."
    except Exception as e:
        return f"Wikipedia lookup failed for '{topic}': {e}"


def get_related_topics(topic: str) -> str:
    """Get topics related to a Wikipedia article."""
    try:
        params = urllib.parse.urlencode({
            "action": "query", "list": "search",
            "srsearch": topic, "srlimit": 5,
            "format": "json"
        })
        url = f"{_SEARCH}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data    = json.loads(resp.read())
        results = data["query"]["search"]
        titles  = [r["title"] for r in results]
        return f"Related topics for '{topic}': " + ", ".join(titles) + ", sir."
    except Exception as e:
        return f"Related topics search failed: {e}"


def on_this_day() -> str:
    """Get interesting events that happened on today's date."""
    today = date.today()
    try:
        url = f"{_API}/feed/onthisday/events/{today.month}/{today.day}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data   = json.loads(resp.read())
        events = data.get("events", [])
        if not events:
            return "No historical events found for today, sir."
        import random
        event = random.choice(events[:10])
        year  = event.get("year", "")
        text  = event.get("text", "")
        return f"On this day in {year}: {text}, sir."
    except Exception as e:
        return f"On this day data unavailable: {e}"


def get_featured_article() -> str:
    """Get today's featured Wikipedia article."""
    today = date.today()
    try:
        url = f"{_API}/feed/featured/{today.year}/{today.month:02d}/{today.day:02d}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        tfa     = data.get("tfa", {})
        title   = tfa.get("title", "Unknown")
        extract = tfa.get("extract", "")[:200]
        return f"Wikipedia featured article: '{title}'. {extract}..., sir."
    except Exception as e:
        return f"Featured article unavailable: {e}"


def search_wikipedia(query: str, limit: int = 3) -> str:
    """Search Wikipedia and return top results."""
    try:
        params = urllib.parse.urlencode({
            "action": "opensearch", "search": query,
            "limit": limit, "format": "json"
        })
        url = f"{_SEARCH}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data  = json.loads(resp.read())
        titles = data[1]
        if not titles:
            return f"No Wikipedia results for '{query}', sir."
        return f"Wikipedia results for '{query}': " + ", ".join(titles) + ", sir."
    except Exception as e:
        return f"Search failed: {e}"
