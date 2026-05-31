"""
jarvis/skills/news.py
News headlines skill — fetches top headlines from RSS feeds.
No API key required. Uses BBC, Reuters and HN as sources.
"""
import urllib.request
import xml.etree.ElementTree as ET


_FEEDS = {
    "world":    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "tech":     "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "science":  "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
}

_DEFAULT_COUNT = 5


def get_headlines(category: str = "world", count: int = _DEFAULT_COUNT) -> str:
    """
    Fetch top headlines for the given category.
    category: world | tech | science | business
    Returns a JARVIS-style spoken summary.
    """
    category = category.lower().strip()
    url = _FEEDS.get(category)
    if url is None:
        # Try a fuzzy match
        for key in _FEEDS:
            if key in category or category in key:
                url = _FEEDS[key]
                category = key
                break
    if url is None:
        url      = _FEEDS["world"]
        category = "world"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read()
        root  = ET.fromstring(raw)
        items = root.findall(".//item")[:count]

        if not items:
            return f"No headlines found in the {category} feed, sir."

        headlines = []
        for i, item in enumerate(items, 1):
            title = item.findtext("title", "").strip()
            if title:
                headlines.append(f"{i}. {title}")

        intro = f"Top {len(headlines)} {category} headlines, sir."
        return intro + " " + ". ".join(h for h in headlines) + "."

    except Exception as e:
        return f"Unable to retrieve headlines at this time: {e}"


def list_categories() -> str:
    cats = ", ".join(_FEEDS.keys())
    return f"Available news categories: {cats}."
