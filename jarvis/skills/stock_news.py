"""Stock news — JARVIS fetches latest financial news headlines."""
import urllib.request, xml.etree.ElementTree as ET, re

_FEEDS = {
    "markets":   "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
    "investing":  "https://www.investing.com/rss/news.rss",
    "reuters":   "https://feeds.reuters.com/reuters/businessNews",
    "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
    "cnbc":      "https://www.cnbc.com/id/10000664/device/rss/rss.html",
}

def get_financial_news(source: str = "cnbc", count: int = 4) -> str:
    url = _FEEDS.get(source.lower(), _FEEDS["cnbc"])
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=7) as resp:
            root  = ET.fromstring(resp.read())
        items  = root.findall(".//item")[:count]
        titles = [re.sub(r"<[^>]+>", "", i.findtext("title", "").strip()) for i in items]
        if not titles: return f"No news from {source}, sir."
        return f"{source.upper()} financial news: " + " | ".join(titles) + ", sir."
    except Exception as e:
        return f"Financial news unavailable: {e}"

def get_market_buzz() -> str:
    """Get a quick markets summary from multiple sources."""
    results = []
    for source in ["cnbc", "reuters"]:
        url = _FEEDS[source]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                root = ET.fromstring(resp.read())
            item  = root.find(".//item")
            title = re.sub(r"<[^>]+>", "", item.findtext("title", "").strip()) if item else ""
            if title: results.append(f"{source.upper()}: {title}")
        except Exception: pass
    if not results: return "Financial news unavailable, sir."
    return "Market buzz: " + " | ".join(results) + ", sir."

def list_sources() -> str:
    return f"Financial news sources: {', '.join(_FEEDS.keys())}, sir."
