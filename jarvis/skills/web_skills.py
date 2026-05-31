"""
jarvis/skills/web_skills.py
Web-based capabilities: DuckDuckGo search, Wikipedia summary,
URL opener, weather via open-meteo (no API key required).
"""
import webbrowser
import urllib.parse
import urllib.request
import json


def web_search(query: str) -> str:
    """Open a DuckDuckGo search in the default browser."""
    encoded = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/?q={encoded}"
    webbrowser.open(url)
    return f"Searching DuckDuckGo for '{query}'..."


def open_url(url: str) -> str:
    """Open an arbitrary URL in the default browser."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url} in your browser."


def wikipedia_summary(topic: str, sentences: int = 2) -> str:
    """
    Fetch a short Wikipedia summary using the free REST API.
    No API key or extra packages needed.
    """
    encoded = urllib.parse.quote(topic.replace(" ", "_"))
    api_url = (
        f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    )
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "JarvisAI/0.2"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        extract = data.get("extract", "")
        if not extract:
            return f"No Wikipedia article found for '{topic}'."
        # Return first N sentences
        parts = extract.split(". ")
        summary = ". ".join(parts[:sentences])
        if not summary.endswith("."):
            summary += "."
        return summary
    except Exception as e:
        return f"Couldn't fetch Wikipedia info: {e}"


def get_weather(location: str = "") -> str:
    """
    Fetch current weather using the open-meteo geocoding + forecast API.
    No API key required.
    """
    try:
        # Step 1: geocode the location
        if location:
            geo_url = (
                f"https://geocoding-api.open-meteo.com/v1/search"
                f"?name={urllib.parse.quote(location)}&count=1"
            )
            req = urllib.request.Request(geo_url, headers={"User-Agent": "JarvisAI/0.2"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                geo = json.loads(resp.read().decode())
            results = geo.get("results", [])
            if not results:
                return f"Couldn't find location: {location}"
            lat  = results[0]["latitude"]
            lon  = results[0]["longitude"]
            name = results[0].get("name", location)
        else:
            # Default to London if no location given
            lat, lon, name = 51.5074, -0.1278, "London"

        # Step 2: fetch current weather
        wx_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
        )
        req = urllib.request.Request(wx_url, headers={"User-Agent": "JarvisAI/0.2"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            wx = json.loads(resp.read().decode())

        cw   = wx["current_weather"]
        temp = cw["temperature"]
        wind = cw["windspeed"]
        code = cw["weathercode"]

        condition = _wmo_description(code)
        return (
            f"Weather in {name}: {condition}, "
            f"{temp}°C, wind {wind} km/h."
        )
    except Exception as e:
        return f"Weather fetch failed: {e}"


# WMO weather interpretation codes (simplified)
_WMO = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "icy fog",
    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
    71: "slight snow", 73: "moderate snow", 75: "heavy snow",
    80: "light showers", 81: "moderate showers", 82: "violent showers",
    95: "thunderstorm", 96: "thunderstorm with hail",
}

def _wmo_description(code: int) -> str:
    return _WMO.get(code, f"weather code {code}")
