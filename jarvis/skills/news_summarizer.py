"""
jarvis/skills/news_summarizer.py
News summarizer — JARVIS fetches and summarises full news articles.
Strips HTML, extracts key sentences, gives a 3-line brief.
"""
import urllib.request
import urllib.parse
import re
import xml.etree.ElementTree as ET


_FEEDS = {
    "world":    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "tech":     "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "science":  "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "health":   "http://feeds.bbci.co.uk/news/health/rss.xml",
    "sports":   "http://feeds.bbci.co.uk/sport/rss.xml",
}


def get_article_summary(url: str) -> str:
    """Fetch a news article URL and return a concise summary."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        text = _strip_html(html)
        text = re.sub(r"\s+", " ", text).strip()
        return _extract_summary(text, sentences=3)
    except Exception as e:
        return f"Could not summarise article: {e}"


def get_top_story(category: str = "world") -> str:
    """Fetch the top story from a category feed and summarise it."""
    feed = _FEEDS.get(category.lower(), _FEEDS["world"])
    try:
        req  = urllib.request.Request(feed, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            root = ET.fromstring(resp.read())
        item = root.find(".//item")
        if item is None:
            return f"No stories found in {category} feed, sir."
        title = item.findtext("title", "").strip()
        desc  = item.findtext("description", "").strip()
        desc  = re.sub(r"<[^>]+>", "", desc)
        desc  = re.sub(r"\s+", " ", desc).strip()[:300]
        return f"Top {category} story: {title}. {desc}, sir."
    except Exception as e:
        return f"Feed error: {e}"


def get_briefing_headlines(categories: list[str] | None = None) -> str:
    """Get one headline from each category for a news briefing."""
    cats   = categories or ["world", "tech", "business"]
    parts  = []
    for cat in cats:
        feed = _FEEDS.get(cat, _FEEDS["world"])
        try:
            req = urllib.request.Request(feed, headers={"User-Agent": "JarvisAI/3.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                root  = ET.fromstring(resp.read())
            item  = root.find(".//item")
            title = item.findtext("title", "").strip() if item else "No story"
            parts.append(f"{cat.upper()}: {title}")
        except Exception:
            pass
    return "News briefing, sir. " + ". ".join(parts) + "."


def _strip_html(html: str) -> str:
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>",  " ", text,  flags=re.DOTALL | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;",   " ", text)
    return text


def _extract_summary(text: str, sentences: int = 3) -> str:
    sents = re.split(r"(?<=[.!?])\s+", text)
    sents = [s.strip() for s in sents if len(s.split()) > 6]
    words = re.findall(r"\w+", text.lower())
    freq  = {}
    for w in words:
        if len(w) > 4:
            freq[w] = freq.get(w, 0) + 1
    scored = sorted(enumerate(sents), key=lambda x: sum(freq.get(w.lower(), 0) for w in x[1].split()), reverse=True)
    top    = sorted(scored[:sentences], key=lambda x: x[0])
    return " ".join(s for _, s in top)
