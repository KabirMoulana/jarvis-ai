"""
jarvis/skills/sports.py
Sports scores and standings — JARVIS reports live scores
for football, cricket, and more via free APIs.
"""
import urllib.request
import json
import os

_FOOTBALL_KEY = os.getenv("FOOTBALL_API_KEY", "")
_API_FOOTBALL = "https://v3.football.api-sports.io"


def get_football_scores(league: str = "premier league") -> str:
    """Get today's football scores."""
    if not _FOOTBALL_KEY:
        return _football_fallback(league)
    try:
        from datetime import date
        today  = date.today().isoformat()
        league_id = _get_league_id(league)
        url    = f"{_API_FOOTBALL}/fixtures?date={today}&league={league_id}&season=2024"
        req    = urllib.request.Request(url, headers={
            "x-apisports-key": _FOOTBALL_KEY,
            "User-Agent": "JarvisAI/3.0"
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        fixtures = data.get("response", [])
        if not fixtures:
            return f"No {league} fixtures today, sir."
        results = []
        for f in fixtures[:5]:
            home  = f["teams"]["home"]["name"]
            away  = f["teams"]["away"]["name"]
            score = f["score"]["fulltime"]
            if score["home"] is not None:
                results.append(f"{home} {score['home']} - {score['away']} {away}")
            else:
                time = f["fixture"]["status"]["short"]
                results.append(f"{home} vs {away} ({time})")
        return f"{league.title()} scores, sir: " + ". ".join(results) + "."
    except Exception as e:
        return _football_fallback(league)


def _football_fallback(league: str) -> str:
    return (
        f"Live {league} scores unavailable, sir. "
        f"Set FOOTBALL_API_KEY in .env for live scores. "
        f"Alternatively, I can open BBC Sport for you."
    )


def _get_league_id(league: str) -> int:
    ids = {
        "premier league": 39, "la liga": 140, "bundesliga": 78,
        "serie a": 135, "ligue 1": 61, "champions league": 2,
        "mls": 253, "world cup": 1
    }
    for key, val in ids.items():
        if key in league.lower():
            return val
    return 39


def get_cricket_scores() -> str:
    """Fetch live cricket scores via Cricbuzz RSS."""
    try:
        url = "https://rss.cricbuzz.com/cb_ltst_crckt_nws"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        import xml.etree.ElementTree as ET
        with urllib.request.urlopen(req, timeout=6) as resp:
            root  = ET.fromstring(resp.read())
        items = root.findall(".//item")[:3]
        if not items:
            return "No cricket news available, sir."
        titles = [i.findtext("title", "").strip() for i in items]
        return "Latest cricket: " + ". ".join(titles) + "."
    except Exception:
        return "Cricket scores unavailable at this time, sir."


def open_sports_news(sport: str = "football") -> str:
    """Open BBC Sport in browser."""
    import webbrowser
    urls = {
        "football": "https://www.bbc.com/sport/football",
        "cricket":  "https://www.bbc.com/sport/cricket",
        "tennis":   "https://www.bbc.com/sport/tennis",
        "formula 1": "https://www.bbc.com/sport/formula1",
        "basketball": "https://www.nba.com",
    }
    url = urls.get(sport.lower(), f"https://www.bbc.com/sport/{sport.lower()}")
    webbrowser.open(url)
    return f"Opening {sport} news, sir."
