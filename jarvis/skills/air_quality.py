"""
jarvis/skills/air_quality.py
Air quality monitor — JARVIS checks AQI and pollution levels.
Uses OpenWeatherMap Air Pollution API (free tier) or WAQI.
"""
import urllib.request
import json
import os

_OWM_KEY  = os.getenv("OPENWEATHER_API_KEY", "")
_WAQI_KEY = os.getenv("WAQI_API_KEY", "demo")

_AQI_LABELS = {
    1: ("Good",        "Air quality is excellent. No health concerns, sir."),
    2: ("Fair",        "Air quality is acceptable. Sensitive groups should limit outdoor activity, sir."),
    3: ("Moderate",    "Air quality is moderate. Consider reducing prolonged outdoor exertion, sir."),
    4: ("Poor",        "Air quality is poor. Limit outdoor activities, sir."),
    5: ("Very Poor",   "Air quality is very poor. Avoid outdoor activity, sir."),
}


def get_air_quality(city: str = "London") -> str:
    """Get current air quality for a city."""
    # Try WAQI API first (free with demo key)
    result = _waqi_aqi(city)
    if result:
        return result

    # Try OpenWeatherMap
    if _OWM_KEY:
        return _owm_aqi(city)

    return (
        f"Air quality data requires an API key, sir. "
        f"Set WAQI_API_KEY or OPENWEATHER_API_KEY in .env. "
        f"Free keys available at waqi.info and openweathermap.org."
    )


def _waqi_aqi(city: str) -> str | None:
    try:
        import urllib.parse
        encoded = urllib.parse.quote(city)
        url     = f"https://api.waqi.info/feed/{encoded}/?token={_WAQI_KEY}"
        req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        if data.get("status") != "ok":
            return None
        aqi    = data["data"]["aqi"]
        label  = _aqi_label(aqi)
        city_n = data["data"].get("city", {}).get("name", city)
        return f"Air quality in {city_n}: AQI {aqi} — {label}, sir."
    except Exception:
        return None


def _owm_aqi(city: str) -> str:
    try:
        import urllib.parse
        # Geocode first
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(city)}&limit=1&appid={_OWM_KEY}"
        req     = urllib.request.Request(geo_url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            geo = json.loads(resp.read())
        if not geo:
            return f"Location '{city}' not found, sir."
        lat, lon = geo[0]["lat"], geo[0]["lon"]
        aqi_url  = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={_OWM_KEY}"
        req      = urllib.request.Request(aqi_url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        aqi   = data["list"][0]["main"]["aqi"]
        label, advice = _AQI_LABELS.get(aqi, ("Unknown", ""))
        return f"Air quality in {city}: {label} (AQI {aqi}). {advice}"
    except Exception as e:
        return f"Air quality check failed: {e}"


def _aqi_label(aqi: int) -> str:
    if aqi <= 50:   return "Good"
    if aqi <= 100:  return "Moderate"
    if aqi <= 150:  return "Unhealthy for sensitive groups"
    if aqi <= 200:  return "Unhealthy"
    if aqi <= 300:  return "Very Unhealthy"
    return "Hazardous"
