
"""Weather command using Open-Meteo (free, no API key needed)."""
import requests


def get_weather(city: str = "Dhaka") -> str:
    """Fetch current weather for a city using Open-Meteo geocoding + forecast."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=5
        ).json()
        if not geo.get("results"):
            return f"I couldn't find weather data for {city}."
        r = geo["results"][0]
        lat, lon = r["latitude"], r["longitude"]
        wx = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current_weather": True,
            },
            timeout=5
        ).json()
        cw = wx["current_weather"]
        temp = cw["temperature"]
        wind = cw["windspeed"]
        return f"In {city}: {temp}°C, wind {wind} km/h."
    except Exception as e:
        return f"Weather fetch failed: {e}"


def handle(command: str) -> str | None:
    if "weather" in command:
        words = command.split()
        # Try to extract a city name after "weather in <city>"
        if "in" in words:
            idx = words.index("in")
            city = " ".join(words[idx + 1:]) or "Dhaka"
        else:
            city = "Dhaka"
        return get_weather(city)
    return None
