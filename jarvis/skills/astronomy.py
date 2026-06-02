"""
jarvis/skills/astronomy.py
Astronomy skill — moon phase, sunrise/sunset, ISS location,
planet visibility. No API key required.
"""
import urllib.request
import json
import math
from datetime import datetime, date, timezone


def get_moon_phase() -> str:
    """Calculate current moon phase using lunar cycle math."""
    known_new_moon = date(2000, 1, 6)
    lunar_cycle    = 29.53058867
    today          = date.today()
    days_since     = (today - known_new_moon).days
    phase_day      = days_since % lunar_cycle

    if phase_day < 1.85:       phase = "New Moon"
    elif phase_day < 7.38:     phase = "Waxing Crescent"
    elif phase_day < 9.22:     phase = "First Quarter"
    elif phase_day < 14.77:    phase = "Waxing Gibbous"
    elif phase_day < 16.61:    phase = "Full Moon"
    elif phase_day < 22.15:    phase = "Waning Gibbous"
    elif phase_day < 23.99:    phase = "Last Quarter"
    elif phase_day < 29.53:    phase = "Waning Crescent"
    else:                      phase = "New Moon"

    illumination = int(abs(math.cos(2 * math.pi * phase_day / lunar_cycle) * -50 + 50))
    return f"The moon is currently in its {phase} phase, sir. Illumination: approximately {illumination}%."


def get_sunrise_sunset(lat: float = 51.5074, lon: float = -0.1278, city: str = "London") -> str:
    """Get sunrise and sunset times for a location using sunrise-sunset.org API."""
    try:
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        results  = data["results"]
        sunrise  = _parse_utc(results["sunrise"])
        sunset   = _parse_utc(results["sunset"])
        day_len  = results["day_length"]
        hours, rem = divmod(day_len, 3600)
        mins, _    = divmod(rem, 60)
        return (
            f"For {city}, sir — sunrise at {sunrise} UTC, "
            f"sunset at {sunset} UTC. "
            f"Day length: {hours} hours {mins} minutes."
        )
    except Exception as e:
        return f"Could not retrieve sun times: {e}"


def get_iss_location() -> str:
    """Get the current location of the International Space Station."""
    try:
        url = "http://api.open-notify.org/iss-now.json"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        pos = data["iss_position"]
        lat = float(pos["latitude"])
        lon = float(pos["longitude"])
        lat_dir = "N" if lat >= 0 else "S"
        lon_dir = "E" if lon >= 0 else "W"
        return (
            f"The International Space Station is currently at "
            f"{abs(lat):.2f}°{lat_dir}, {abs(lon):.2f}°{lon_dir}, sir. "
            f"Moving at approximately 28,000 kilometres per hour."
        )
    except Exception as e:
        return f"Could not retrieve ISS location: {e}"


def get_iss_crew() -> str:
    """Get current ISS crew members."""
    try:
        url = "http://api.open-notify.org/astros.json"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        iss_crew = [p["name"] for p in data["people"] if p["craft"] == "ISS"]
        if not iss_crew:
            return "No crew data available for the ISS, sir."
        return (
            f"There are currently {len(iss_crew)} astronauts aboard the ISS, sir: "
            + ", ".join(iss_crew) + "."
        )
    except Exception as e:
        return f"Could not retrieve crew data: {e}"


def astronomy_fact() -> str:
    """Return a random astronomy fact."""
    facts = [
        "The Sun contains 99.86% of the mass in our solar system, sir.",
        "Light from the Sun takes 8 minutes and 20 seconds to reach Earth, sir.",
        "A neutron star can spin 600 times per second, sir.",
        "The Milky Way has an estimated 100 to 400 billion stars, sir.",
        "There are more stars in the universe than grains of sand on all Earth's beaches, sir.",
        "The ISS orbits Earth every 90 minutes at 7.7 kilometres per second, sir.",
        "One day on Venus is longer than one year on Venus, sir.",
        "The footprints on the Moon will last for 100 million years, sir.",
        "Jupiter's Great Red Spot has been raging for over 350 years, sir.",
    ]
    import random
    return random.choice(facts)


def _parse_utc(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%H:%M")
    except Exception:
        return dt_str
