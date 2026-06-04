"""
jarvis/skills/location_finder.py
Location finder — JARVIS finds nearby places using
Nominatim (OSM) and Overpass API. No key required.
"""
import urllib.request
import urllib.parse
import json
import webbrowser


_NOMINATIM = "https://nominatim.openstreetmap.org"
_OVERPASS  = "https://overpass-api.de/api/interpreter"


def geocode(address: str) -> dict | None:
    """Convert address to coordinates."""
    try:
        encoded = urllib.parse.quote(address)
        url     = f"{_NOMINATIM}/search?q={encoded}&format=json&limit=1"
        req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        if data:
            return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"]),
                    "display": data[0]["display_name"]}
    except Exception:
        pass
    return None


def find_nearby(place_type: str, location: str, radius_m: int = 1000) -> str:
    """Find nearby places of a given type near a location."""
    coords = geocode(location)
    if not coords:
        return f"Could not find coordinates for '{location}', sir."

    lat, lon = coords["lat"], coords["lon"]
    tag_map  = {
        "restaurant": "amenity=restaurant",
        "cafe":       "amenity=cafe",
        "hospital":   "amenity=hospital",
        "pharmacy":   "amenity=pharmacy",
        "atm":        "amenity=atm",
        "bank":       "amenity=bank",
        "hotel":      "tourism=hotel",
        "gym":        "leisure=fitness_centre",
        "park":       "leisure=park",
        "school":     "amenity=school",
        "supermarket":"shop=supermarket",
        "petrol":     "amenity=fuel",
    }
    tag = tag_map.get(place_type.lower(), f"amenity={place_type.lower()}")
    query = f"""
    [out:json][timeout:10];
    node[{tag}](around:{radius_m},{lat},{lon});
    out 5;
    """
    try:
        data  = urllib.parse.urlencode({"data": query}).encode()
        req   = urllib.request.Request(_OVERPASS, data=data, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            result  = json.loads(resp.read())
        elements = result.get("elements", [])
        if not elements:
            return f"No {place_type}s found near {location} within {radius_m}m, sir."
        names = [e.get("tags", {}).get("name", "Unnamed") for e in elements[:5]]
        return f"Nearby {place_type}s near {location}: " + ", ".join(names) + ", sir."
    except Exception as e:
        return f"Location search failed: {e}"


def open_google_maps(location: str) -> str:
    """Open Google Maps for a location."""
    encoded = urllib.parse.quote(location)
    webbrowser.open(f"https://www.google.com/maps/search/{encoded}")
    return f"Opening Google Maps for '{location}', sir."


def get_address_from_coords(lat: float, lon: float) -> str:
    """Reverse geocode — get address from coordinates."""
    try:
        url = f"{_NOMINATIM}/reverse?lat={lat}&lon={lon}&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        return f"Coordinates {lat}, {lon} is {data.get('display_name', 'Unknown')}, sir."
    except Exception as e:
        return f"Reverse geocode failed: {e}"
