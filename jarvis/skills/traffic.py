"""
jarvis/skills/traffic.py
Traffic and travel time estimates — JARVIS checks your commute.
Uses OpenRouteService free API (no key needed for basic use)
and falls back to estimated travel times.
"""
import urllib.request
import urllib.parse
import json
import os

_ORS_KEY = os.getenv("OPENROUTESERVICE_API_KEY", "")
_ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_travel_time(origin: str, destination: str) -> str:
    """Estimate travel time between two locations."""
    if _ORS_KEY:
        return _ors_directions(origin, destination)
    return _fallback_estimate(origin, destination)


def _ors_directions(origin: str, destination: str) -> str:
    try:
        # Geocode both locations first
        orig_coords = _geocode(origin)
        dest_coords = _geocode(destination)
        if not orig_coords or not dest_coords:
            return f"Could not geocode locations, sir."

        payload = json.dumps({
            "coordinates": [orig_coords, dest_coords]
        }).encode()

        req = urllib.request.Request(
            _ORS_URL,
            data=payload,
            headers={
                "Authorization": _ORS_KEY,
                "Content-Type":  "application/json",
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())

        summary  = data["routes"][0]["summary"]
        distance = summary["distance"] / 1000
        duration = summary["duration"] / 60

        return (
            f"Travel time from {origin} to {destination}: "
            f"{duration:.0f} minutes by car, "
            f"{distance:.1f} km, sir."
        )
    except Exception as e:
        return _fallback_estimate(origin, destination)


def _geocode(location: str) -> list | None:
    try:
        encoded = urllib.parse.quote(location)
        url     = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1"
        req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        if data:
            return [float(data[0]["lon"]), float(data[0]["lat"])]
    except Exception:
        pass
    return None


def _fallback_estimate(origin: str, destination: str) -> str:
    return (
        f"I don't have live traffic data for that route, sir. "
        f"For travel time from {origin} to {destination}, "
        f"I'd recommend checking Google Maps. "
        f"Set OPENROUTESERVICE_API_KEY in .env for live estimates."
    )


def get_commute_time(home: str = "", work: str = "") -> str:
    """Get commute time using saved home/work locations."""
    h = home or os.getenv("JARVIS_HOME_LOCATION", "")
    w = work or os.getenv("JARVIS_WORK_LOCATION", "")
    if not h or not w:
        return (
            "Home and work locations not set, sir. "
            "Add JARVIS_HOME_LOCATION and JARVIS_WORK_LOCATION to your .env file."
        )
    return get_travel_time(h, w)


def open_maps(origin: str, destination: str) -> str:
    """Open Google Maps directions in browser."""
    import webbrowser
    o = urllib.parse.quote(origin)
    d = urllib.parse.quote(destination)
    webbrowser.open(f"https://www.google.com/maps/dir/{o}/{d}")
    return f"Opening Google Maps directions from {origin} to {destination}, sir."
