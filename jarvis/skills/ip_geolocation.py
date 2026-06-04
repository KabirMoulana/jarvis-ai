"""
jarvis/skills/ip_geolocation.py
IP geolocation — JARVIS looks up location data for any IP address.
Uses ip-api.com (free, no key, 1000 req/min limit).
"""
import urllib.request
import json


_API = "http://ip-api.com/json"


def geolocate_ip(ip: str = "") -> str:
    """
    Get geolocation for an IP address.
    Leave ip empty to geolocate your own public IP.
    """
    endpoint = f"{_API}/{ip}" if ip else f"{_API}"
    try:
        req = urllib.request.Request(endpoint, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())

        if data.get("status") != "success":
            return f"Could not geolocate {ip or 'your IP'}, sir."

        target   = ip or data.get("query", "your IP")
        city     = data.get("city", "Unknown")
        region   = data.get("regionName", "")
        country  = data.get("country", "Unknown")
        isp      = data.get("isp", "Unknown")
        lat      = data.get("lat", 0)
        lon      = data.get("lon", 0)
        timezone = data.get("timezone", "")

        return (
            f"{target} is located in {city}, {region}, {country}, sir. "
            f"ISP: {isp}. "
            f"Coordinates: {lat:.2f}, {lon:.2f}. "
            f"Timezone: {timezone}."
        )
    except Exception as e:
        return f"Geolocation failed: {e}"


def get_my_location() -> str:
    """Get your own location based on public IP."""
    return geolocate_ip("")


def get_country_info(country: str) -> str:
    """Get basic info about a country using REST Countries API."""
    try:
        url = f"https://restcountries.com/v3.1/name/{urllib.request.quote(country)}?fields=name,capital,population,area,currencies,languages,flags"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        c        = data[0]
        name     = c["name"]["common"]
        capital  = c.get("capital", ["Unknown"])[0]
        pop      = f"{c.get('population', 0):,}"
        langs    = ", ".join(list(c.get("languages", {}).values())[:3])
        currencies = ", ".join(v["name"] for v in c.get("currencies", {}).values())
        return (
            f"{name}: capital {capital}, population {pop}. "
            f"Languages: {langs}. Currency: {currencies}, sir."
        )
    except Exception as e:
        return f"Country lookup failed: {e}"
