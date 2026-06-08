"""Solar system explorer — JARVIS gives planet facts."""
_PLANETS = {
    "mercury": {"distance_km": 57.9e6, "moons": 0, "day_hours": 1408, "year_days": 88, "temp_c": 167, "fact": "Mercury has no atmosphere and extreme temperature swings."},
    "venus":   {"distance_km": 108.2e6, "moons": 0, "day_hours": 5832, "year_days": 225, "temp_c": 464, "fact": "Venus is the hottest planet despite not being closest to the Sun."},
    "earth":   {"distance_km": 149.6e6, "moons": 1, "day_hours": 24, "year_days": 365, "temp_c": 15, "fact": "Earth is the only known planet with life."},
    "mars":    {"distance_km": 227.9e6, "moons": 2, "day_hours": 24.6, "year_days": 687, "temp_c": -65, "fact": "Mars has the tallest volcano in the solar system — Olympus Mons."},
    "jupiter": {"distance_km": 778.5e6, "moons": 95, "day_hours": 9.9, "year_days": 4333, "temp_c": -110, "fact": "Jupiter's Great Red Spot is a storm that has lasted over 350 years."},
    "saturn":  {"distance_km": 1432e6, "moons": 146, "day_hours": 10.7, "year_days": 10759, "temp_c": -140, "fact": "Saturn's rings are made of ice and rock particles."},
    "uranus":  {"distance_km": 2867e6, "moons": 27, "day_hours": 17.2, "year_days": 30687, "temp_c": -195, "fact": "Uranus rotates on its side with an axial tilt of 98 degrees."},
    "neptune": {"distance_km": 4515e6, "moons": 16, "day_hours": 16.1, "year_days": 60190, "temp_c": -200, "fact": "Neptune has the strongest winds in the solar system at 2,100 km/h."},
}

def get_planet(name: str) -> str:
    p = _PLANETS.get(name.lower().strip())
    if not p:
        planets = ", ".join(_PLANETS.keys())
        return f"Planet '{name}' not found, sir. Planets: {planets}."
    return (f"{name.title()}: {p['moons']} moon(s), {p['year_days']:.0f}-day year, "
            f"average {p['temp_c']}°C. {p['fact']}, sir.")

def compare_planets(p1: str, p2: str) -> str:
    d1 = _PLANETS.get(p1.lower())
    d2 = _PLANETS.get(p2.lower())
    if not d1 or not d2:
        return "One or both planets not found, sir."
    return (f"{p1.title()} vs {p2.title()}, sir: "
            f"Moons: {d1['moons']} vs {d2['moons']}. "
            f"Year length: {d1['year_days']:.0f} vs {d2['year_days']:.0f} days. "
            f"Temperature: {d1['temp_c']}°C vs {d2['temp_c']}°C.")

def list_planets() -> str:
    return "Solar system planets: " + ", ".join(p.title() for p in _PLANETS) + ", sir."
