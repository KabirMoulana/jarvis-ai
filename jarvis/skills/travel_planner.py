"""
jarvis/skills/travel_planner.py
Travel planner — JARVIS helps plan trips.
Currency, time zones, visa info, packing lists, weather.
"""
import urllib.request
import json
import webbrowser
import urllib.parse


_VISA_FREE = {
    "uk": ["usa", "canada", "australia", "japan", "germany", "france", "italy"],
    "usa": ["uk", "canada", "australia", "japan", "germany", "france"],
    "india": ["nepal", "bhutan", "maldives", "mauritius"],
}


def get_trip_overview(destination: str, origin: str = "") -> str:
    """Give a travel overview for a destination."""
    dest = destination.strip()
    parts = [f"Travel overview for {dest}, sir."]

    # Time zone
    try:
        from jarvis.skills.world_clock import get_time_in
        time_info = get_time_in(dest)
        parts.append(time_info)
    except Exception:
        pass

    # Weather
    try:
        from jarvis.skills.web_skills import get_weather
        weather = get_weather(dest)
        parts.append(weather)
    except Exception:
        pass

    return " ".join(parts)


def get_packing_list(trip_type: str = "general", days: int = 7) -> str:
    """Generate a packing list for a trip type."""
    lists = {
        "beach": ["sunscreen", "swimwear", "flip flops", "sunglasses", "beach towel", "hat", "light clothing"],
        "business": ["suits/formal wear", "laptop", "chargers", "business cards", "dress shoes", "ties"],
        "hiking": ["hiking boots", "backpack", "water bottle", "first aid kit", "map", "torch", "rain jacket"],
        "general": ["passport", "phone charger", "medications", "underwear", "t-shirts", "toiletries", "camera"],
        "winter": ["heavy coat", "thermal wear", "gloves", "scarf", "boots", "wool socks", "hat"],
        "camping": ["tent", "sleeping bag", "camp stove", "bug spray", "matches", "rope", "knife"],
    }
    trip_type = trip_type.lower()
    items     = lists.get(trip_type, lists["general"])
    if days > 7:
        items.append("laundry bag")
    return f"Packing list for {days}-day {trip_type} trip: " + ", ".join(items) + ", sir."


def search_flights(origin: str, destination: str) -> str:
    """Open Google Flights for a route."""
    o = urllib.parse.quote(origin)
    d = urllib.parse.quote(destination)
    webbrowser.open(f"https://www.google.com/flights?q=Flights+from+{o}+to+{d}")
    return f"Opening Google Flights from {origin} to {destination}, sir."


def search_hotels(destination: str, check_in: str = "", check_out: str = "") -> str:
    """Open Booking.com for hotel search."""
    d = urllib.parse.quote(destination)
    webbrowser.open(f"https://www.booking.com/search.html?ss={d}")
    return f"Opening Booking.com for hotels in {destination}, sir."


def get_travel_tips(destination: str) -> str:
    """Return generic travel safety tips."""
    return (
        f"Travel tips for {destination}, sir. "
        f"Check visa requirements before travel. "
        f"Carry copies of your passport. "
        f"Inform your bank of travel dates. "
        f"Get travel insurance. "
        f"Download offline maps. "
        f"Keep emergency contacts saved."
    )


def convert_travel_currency(amount: float, from_cur: str, to_cur: str) -> str:
    """Quick currency conversion for travel."""
    from jarvis.skills.currency import convert_currency
    return convert_currency(amount, from_cur, to_cur)
