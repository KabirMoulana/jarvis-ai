"""
jarvis/skills/podcast_finder.py
Podcast finder — JARVIS searches and opens podcast episodes.
Uses the iTunes/Apple Podcasts search API (free, no key).
"""
import urllib.request
import urllib.parse
import json
import webbrowser


_ITUNES_API = "https://itunes.apple.com/search"


def search_podcasts(query: str, limit: int = 5) -> str:
    """Search for podcasts by name or topic."""
    try:
        params = urllib.parse.urlencode({
            "term":      query,
            "media":     "podcast",
            "limit":     limit,
            "entity":    "podcast",
        })
        url = f"{_ITUNES_API}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data    = json.loads(resp.read())
        results = data.get("results", [])
        if not results:
            return f"No podcasts found for '{query}', sir."
        names = [r["collectionName"] for r in results[:5]]
        return f"Podcasts matching '{query}': " + ", ".join(names) + ", sir."
    except Exception as e:
        return f"Podcast search failed: {e}"


def search_episodes(podcast_name: str, limit: int = 3) -> str:
    """Search for episodes of a specific podcast."""
    try:
        params = urllib.parse.urlencode({
            "term":   podcast_name,
            "media":  "podcast",
            "entity": "podcastEpisode",
            "limit":  limit,
        })
        url = f"{_ITUNES_API}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data    = json.loads(resp.read())
        results = data.get("results", [])
        episodes = [r for r in results if r.get("kind") == "podcast-episode"]
        if not episodes:
            return f"No episodes found for '{podcast_name}', sir."
        titles = [e.get("trackName", "Unknown") for e in episodes[:3]]
        return f"Recent episodes of {podcast_name}: " + "; ".join(titles) + ", sir."
    except Exception as e:
        return f"Episode search failed: {e}"


def open_podcast(podcast_name: str) -> str:
    """Open Spotify search for a podcast."""
    encoded = urllib.parse.quote(podcast_name)
    webbrowser.open(f"https://open.spotify.com/search/{encoded}/podcasts")
    return f"Opening '{podcast_name}' on Spotify Podcasts, sir."


def get_top_tech_podcasts() -> str:
    """Return a curated list of top tech podcasts."""
    top = [
        "Lex Fridman Podcast",
        "The Tim Ferriss Show",
        "How I Built This",
        "Masters of Scale",
        "StartUp Podcast",
        "Darknet Diaries",
        "Software Engineering Daily",
        "Huberman Lab",
    ]
    return "Top tech and science podcasts, sir: " + ", ".join(top) + "."
