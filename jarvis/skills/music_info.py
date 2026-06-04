"""
jarvis/skills/music_info.py
Music information — JARVIS looks up artist info, album details,
and lyrics summaries using MusicBrainz (free, no key).
"""
import urllib.request
import urllib.parse
import json
import webbrowser


_MB_API = "https://musicbrainz.org/ws/2"
_HEADERS = {
    "User-Agent":  "JarvisAI/3.0 (kabirmoulana@github)",
    "Accept":      "application/json",
}


def get_artist_info(artist: str) -> str:
    """Look up information about an artist."""
    try:
        params = urllib.parse.urlencode({"query": artist, "limit": 1, "fmt": "json"})
        url    = f"{_MB_API}/artist?{params}"
        req    = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=6) as resp:
            data    = json.loads(resp.read())
        artists = data.get("artists", [])
        if not artists:
            return f"No artist found for '{artist}', sir."
        a       = artists[0]
        name    = a.get("name", artist)
        country = a.get("area", {}).get("name", "Unknown")
        genre   = ", ".join(t.get("name", "") for t in a.get("tags", [])[:3]) or "Unknown"
        score   = a.get("score", 0)
        return (
            f"Artist: {name}. Country: {country}. "
            f"Genre tags: {genre}. Confidence: {score}%, sir."
        )
    except Exception as e:
        return f"Artist lookup failed: {e}"


def search_song(song: str, artist: str = "") -> str:
    """Search for a song."""
    query = f"{song} {artist}".strip()
    try:
        params = urllib.parse.urlencode({"query": query, "limit": 3, "fmt": "json"})
        url    = f"{_MB_API}/recording?{params}"
        req    = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        recordings = data.get("recordings", [])
        if not recordings:
            return f"No results found for '{query}', sir."
        results = []
        for r in recordings[:3]:
            title  = r.get("title", "Unknown")
            artist_credit = r.get("artist-credit", [{}])[0].get("artist", {}).get("name", "Unknown")
            results.append(f"'{title}' by {artist_credit}")
        return "Found: " + "; ".join(results) + ", sir."
    except Exception as e:
        return f"Song search failed: {e}"


def open_lyrics(song: str, artist: str = "") -> str:
    """Open lyrics search on Genius."""
    query   = urllib.parse.quote(f"{artist} {song}".strip())
    webbrowser.open(f"https://genius.com/search?q={query}")
    return f"Opening Genius for '{song}' lyrics, sir."


def open_spotify_artist(artist: str) -> str:
    """Open Spotify artist page."""
    encoded = urllib.parse.quote(artist)
    webbrowser.open(f"https://open.spotify.com/search/{encoded}/artists")
    return f"Opening {artist} on Spotify, sir."


def get_music_charts() -> str:
    """Open Billboard Hot 100."""
    webbrowser.open("https://www.billboard.com/charts/hot-100/")
    return "Opening Billboard Hot 100 charts, sir."
