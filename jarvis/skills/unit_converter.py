"""
jarvis/skills/unit_converter.py
Comprehensive unit converter — JARVIS handles any conversion by voice.
Covers: length, weight, temperature, speed, area, volume, data, time, currency.
"""
import re

# ── Conversion tables (to SI base unit) ───────────────────────────────────────
_CONVERSIONS: dict[str, dict[str, float]] = {
    "length": {
        "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
        "inch": 0.0254, "inches": 0.0254, "foot": 0.3048, "feet": 0.3048,
        "ft": 0.3048, "yard": 0.9144, "yards": 0.9144, "mile": 1609.344, "miles": 1609.344,
    },
    "weight": {
        "mg": 0.000001, "g": 0.001, "kg": 1, "tonne": 1000,
        "oz": 0.028349, "ounce": 0.028349, "lb": 0.453592, "lbs": 0.453592,
        "pound": 0.453592, "pounds": 0.453592, "stone": 6.350293,
    },
    "speed": {
        "mph": 0.44704, "kph": 0.27778, "kmh": 0.27778,
        "knot": 0.51444, "mps": 1,
    },
    "area": {
        "mm2": 1e-6, "cm2": 1e-4, "m2": 1, "km2": 1e6,
        "sqft": 0.092903, "sqin": 0.000645, "acre": 4046.856,
        "hectare": 10000, "sqmile": 2589988,
    },
    "volume": {
        "ml": 0.001, "l": 1, "litre": 1, "liter": 1,
        "cup": 0.236588, "pint": 0.473176, "quart": 0.946353,
        "gallon": 3.785411, "floz": 0.029574, "tbsp": 0.014787, "tsp": 0.004929,
    },
    "data": {
        "bit": 0.125, "byte": 1, "kb": 1024, "mb": 1048576,
        "gb": 1073741824, "tb": 1099511627776, "pb": 1125899906842624,
    },
    "time": {
        "second": 1, "minute": 60, "hour": 3600,
        "day": 86400, "week": 604800, "month": 2629800, "year": 31557600,
    },
}


def convert(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value from one unit to another."""
    from_u = from_unit.lower().strip()
    to_u   = to_unit.lower().strip()

    # Temperature — special case
    if from_u in ("c", "celsius", "°c") or to_u in ("c", "celsius", "°c") \
    or from_u in ("f", "fahrenheit", "°f") or to_u in ("f", "fahrenheit", "°f") \
    or from_u in ("k", "kelvin") or to_u in ("k", "kelvin"):
        return _convert_temperature(value, from_u, to_u)

    # Find category
    for category, units in _CONVERSIONS.items():
        if from_u in units and to_u in units:
            base   = value * units[from_u]
            result = base / units[to_u]
            result = round(result, 4) if result != int(result) else int(result)
            return f"{value} {from_unit} = {result:,} {to_unit}, sir."

    return f"I don't know how to convert {from_unit} to {to_unit}, sir."


def _convert_temperature(value: float, from_u: str, to_u: str) -> str:
    # Normalise aliases
    _c = ("c", "celsius", "°c")
    _f = ("f", "fahrenheit", "°f")
    _k = ("k", "kelvin")

    if from_u in _c:
        celsius = value
    elif from_u in _f:
        celsius = (value - 32) * 5/9
    elif from_u in _k:
        celsius = value - 273.15
    else:
        return f"Unknown temperature unit: {from_u}"

    if to_u in _c:
        result, unit = celsius, "°C"
    elif to_u in _f:
        result, unit = celsius * 9/5 + 32, "°F"
    elif to_u in _k:
        result, unit = celsius + 273.15, "K"
    else:
        return f"Unknown temperature unit: {to_u}"

    return f"{value} {from_u.upper()} = {result:.2f} {unit}, sir."


def parse_conversion(text: str) -> str:
    """Parse 'convert 5 km to miles' or '100 fahrenheit in celsius'."""
    m = re.search(
        r"(\d+\.?\d*)\s*([\w°]+)\s+(?:to|in(?:to)?)\s+([\w°]+)",
        text, re.IGNORECASE
    )
    if m:
        value     = float(m.group(1))
        from_unit = m.group(2)
        to_unit   = m.group(3)
        return convert(value, from_unit, to_unit)
    return "Please say something like 'convert 5 km to miles', sir."
