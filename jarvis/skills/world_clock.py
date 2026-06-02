"""
jarvis/skills/world_clock.py
World clock — current time in any city or timezone.
No API key required — uses Python's zoneinfo.
"""
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import re

_CITY_ZONES = {
    "new york":       "America/New_York",
    "los angeles":    "America/Los_Angeles",
    "chicago":        "America/Chicago",
    "london":         "Europe/London",
    "paris":          "Europe/Paris",
    "berlin":         "Europe/Berlin",
    "dubai":          "Asia/Dubai",
    "mumbai":         "Asia/Kolkata",
    "delhi":          "Asia/Kolkata",
    "kolkata":        "Asia/Kolkata",
    "colombo":        "Asia/Colombo",
    "singapore":      "Asia/Singapore",
    "hong kong":      "Asia/Hong_Kong",
    "tokyo":          "Asia/Tokyo",
    "seoul":          "Asia/Seoul",
    "sydney":         "Australia/Sydney",
    "melbourne":      "Australia/Melbourne",
    "auckland":       "Pacific/Auckland",
    "moscow":         "Europe/Moscow",
    "beijing":        "Asia/Shanghai",
    "shanghai":       "Asia/Shanghai",
    "istanbul":       "Europe/Istanbul",
    "cairo":          "Africa/Cairo",
    "johannesburg":   "Africa/Johannesburg",
    "nairobi":        "Africa/Nairobi",
    "toronto":        "America/Toronto",
    "vancouver":      "America/Vancouver",
    "mexico city":    "America/Mexico_City",
    "sao paulo":      "America/Sao_Paulo",
    "buenos aires":   "America/Argentina/Buenos_Aires",
    "riyadh":         "Asia/Riyadh",
    "karachi":        "Asia/Karachi",
    "dhaka":          "Asia/Dhaka",
    "bangkok":        "Asia/Bangkok",
    "jakarta":        "Asia/Jakarta",
    "kuala lumpur":   "Asia/Kuala_Lumpur",
    "lahore":         "Asia/Karachi",
    "tehran":         "Asia/Tehran",
    "baghdad":        "Asia/Baghdad",
    "amsterdam":      "Europe/Amsterdam",
    "rome":           "Europe/Rome",
    "madrid":         "Europe/Madrid",
    "zurich":         "Europe/Zurich",
    "stockholm":      "Europe/Stockholm",
    "oslo":           "Europe/Oslo",
    "helsinki":       "Europe/Helsinki",
    "warsaw":         "Europe/Warsaw",
    "prague":         "Europe/Prague",
    "vienna":         "Europe/Vienna",
}


def get_time_in(location: str) -> str:
    """Return the current time in the given city or timezone."""
    loc_lower = location.lower().strip()

    # Exact city match
    tz_str = _CITY_ZONES.get(loc_lower)

    # Partial match
    if not tz_str:
        for city, tz in _CITY_ZONES.items():
            if loc_lower in city or city in loc_lower:
                tz_str = tz
                location = city.title()
                break

    # Try as raw timezone string (e.g. "America/New_York")
    if not tz_str:
        tz_str = location

    try:
        tz   = ZoneInfo(tz_str)
        now  = datetime.now(tz)
        time = now.strftime("%I:%M %p")
        day  = now.strftime("%A, %B %d")
        return f"It is currently {time} on {day} in {location.title()}, sir."
    except ZoneInfoNotFoundError:
        return f"I don't recognise '{location}' as a city or timezone, sir."
    except Exception as e:
        return f"Could not get time for {location}: {e}"


def get_multiple_times(cities: list[str]) -> str:
    """Return times for multiple cities at once."""
    results = []
    for city in cities:
        result = get_time_in(city)
        results.append(result)
    return " ".join(results)


def list_supported_cities() -> str:
    cities = ", ".join(c.title() for c in list(_CITY_ZONES.keys())[:15])
    return f"Supported cities include: {cities}, and many more, sir."


def get_timezone_offset(location: str) -> str:
    """Return the UTC offset for a location."""
    loc_lower = location.lower().strip()
    tz_str    = _CITY_ZONES.get(loc_lower, location)
    try:
        tz     = ZoneInfo(tz_str)
        now    = datetime.now(tz)
        offset = now.utcoffset()
        hours  = int(offset.total_seconds() // 3600)
        mins   = int((offset.total_seconds() % 3600) // 60)
        sign   = "+" if hours >= 0 else ""
        return f"{location.title()} is UTC{sign}{hours}:{mins:02d}, sir."
    except Exception:
        return f"Could not determine timezone for {location}, sir."
