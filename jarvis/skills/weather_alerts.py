"""
jarvis/skills/weather_alerts.py
Weather alerts — JARVIS monitors weather and warns of bad conditions.
Uses Open-Meteo free API for hourly forecasts.
"""
import urllib.request
import json
from datetime import datetime


_WEATHER_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "icy fog", 51: "light drizzle", 53: "moderate drizzle",
    55: "heavy drizzle", 61: "light rain", 63: "moderate rain", 65: "heavy rain",
    71: "light snow", 73: "moderate snow", 75: "heavy snow", 80: "light showers",
    81: "moderate showers", 82: "violent showers", 95: "thunderstorm",
    96: "thunderstorm with hail", 99: "thunderstorm with heavy hail",
}

_ALERT_CODES = {95, 96, 99, 65, 75, 82}


def get_hourly_forecast(lat: float = 51.5074, lon: float = -0.1278,
                        city: str = "London", hours: int = 6) -> str:
    """Get hourly weather forecast."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&hourly=temperature_2m,weathercode,precipitation_probability"
            f"&forecast_days=1&timezone=auto"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())

        hourly  = data["hourly"]
        times   = hourly["time"][:hours]
        temps   = hourly["temperature_2m"][:hours]
        codes   = hourly["weathercode"][:hours]
        precip  = hourly["precipitation_probability"][:hours]

        now_hour = datetime.now().hour
        parts    = []
        for i, (t, temp, code, rain) in enumerate(zip(times, temps, codes, precip)):
            hour_str = datetime.fromisoformat(t).strftime("%I%p")
            cond     = _WEATHER_CODES.get(code, "unknown")
            parts.append(f"{hour_str}: {temp:.0f}°C {cond} {rain}% rain")

        return f"Next {hours} hours in {city}: " + " | ".join(parts) + ", sir."
    except Exception as e:
        return f"Forecast unavailable: {e}"


def check_weather_alerts(lat: float = 51.5074, lon: float = -0.1278,
                         city: str = "London") -> str:
    """Check for severe weather alerts."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&hourly=weathercode&forecast_days=1&timezone=auto"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data  = json.loads(resp.read())
        codes = data["hourly"]["weathercode"][:24]
        alerts = [_WEATHER_CODES[c] for c in codes if c in _ALERT_CODES]
        if alerts:
            return (
                f"Weather alert for {city}, sir! "
                f"Severe conditions expected: {', '.join(set(alerts))}. "
                f"Plan accordingly."
            )
        return f"No severe weather alerts for {city} today, sir."
    except Exception as e:
        return f"Alert check failed: {e}"


def get_uv_index(lat: float = 51.5074, lon: float = -0.1278) -> str:
    """Get UV index for the day."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=uv_index_max&forecast_days=1&timezone=auto"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        uv = data["daily"]["uv_index_max"][0]
        level = "low" if uv < 3 else "moderate" if uv < 6 else "high" if uv < 8 else "very high" if uv < 11 else "extreme"
        advice = "" if uv < 3 else " Wear sunscreen, sir." if uv < 6 else " Limit sun exposure, sir."
        return f"UV index today: {uv:.0f} ({level}).{advice}"
    except Exception as e:
        return f"UV data unavailable: {e}"
