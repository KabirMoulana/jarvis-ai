"""
jarvis/skills/satellite_tracker.py
Satellite tracker — JARVIS tracks satellites and space objects.
Uses N2YO free API and Open Notify for ISS passes.
"""
import urllib.request
import json
import os
from datetime import datetime

_N2YO_KEY = os.getenv("N2YO_API_KEY", "")
_OPEN_NOTIFY = "http://api.open-notify.org"


def get_iss_pass_times(lat: float = 51.5074, lon: float = -0.1278,
                       alt: int = 0, city: str = "London") -> str:
    """Get next ISS pass times over a location."""
    try:
        url = f"{_OPEN_NOTIFY}/iss-pass.json?lat={lat}&lon={lon}&alt={alt}&n=3"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        passes = data.get("response", [])
        if not passes:
            return f"No ISS passes predicted for {city} in the near future, sir."
        parts = []
        for p in passes:
            rise_time = datetime.fromtimestamp(p["risetime"]).strftime("%d %b %H:%M")
            duration  = p["duration"]
            parts.append(f"{rise_time} for {duration}s")
        return (
            f"Next ISS passes over {city}, sir: "
            + " | ".join(parts) + "."
        )
    except Exception as e:
        return f"ISS pass data unavailable: {e}"


def get_iss_current_position() -> str:
    """Get real-time ISS position."""
    try:
        url = f"{_OPEN_NOTIFY}/iss-now.json"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        pos = data["iss_position"]
        lat = float(pos["latitude"])
        lon = float(pos["longitude"])
        lat_dir = "N" if lat >= 0 else "S"
        lon_dir = "E" if lon >= 0 else "W"
        return (
            f"ISS is currently at {abs(lat):.2f}°{lat_dir}, "
            f"{abs(lon):.2f}°{lon_dir}, sir. "
            f"Travelling at approximately 27,600 km/h."
        )
    except Exception as e:
        return f"ISS position unavailable: {e}"


def get_space_weather() -> str:
    """Fetch current space weather / solar activity."""
    try:
        url = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        latest = data[-1] if data else {}
        ssn    = latest.get("ssn", "N/A")
        return (
            f"Current solar cycle data, sir: "
            f"Sunspot number: {ssn}. "
            f"Space weather conditions sourced from NOAA."
        )
    except Exception as e:
        return f"Space weather data unavailable: {e}"


def get_astronomy_picture() -> str:
    """Get NASA Astronomy Picture of the Day info."""
    nasa_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        title = data.get("title", "Unknown")
        expl  = data.get("explanation", "")[:150]
        date  = data.get("date", "")
        return (
            f"NASA Astronomy Picture of the Day ({date}): '{title}'. "
            f"{expl}..., sir."
        )
    except Exception as e:
        return f"NASA APOD unavailable: {e}"
