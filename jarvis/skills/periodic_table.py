"""
jarvis/skills/periodic_table.py
Periodic table — JARVIS looks up element info by name or symbol.
Full data for all 118 elements, no API needed.
"""

_ELEMENTS = {
    "H":  {"name": "Hydrogen",   "number": 1,   "mass": 1.008,   "category": "nonmetal"},
    "He": {"name": "Helium",     "number": 2,   "mass": 4.003,   "category": "noble gas"},
    "Li": {"name": "Lithium",    "number": 3,   "mass": 6.941,   "category": "alkali metal"},
    "Be": {"name": "Beryllium",  "number": 4,   "mass": 9.012,   "category": "alkaline earth metal"},
    "B":  {"name": "Boron",      "number": 5,   "mass": 10.811,  "category": "metalloid"},
    "C":  {"name": "Carbon",     "number": 6,   "mass": 12.011,  "category": "nonmetal"},
    "N":  {"name": "Nitrogen",   "number": 7,   "mass": 14.007,  "category": "nonmetal"},
    "O":  {"name": "Oxygen",     "number": 8,   "mass": 15.999,  "category": "nonmetal"},
    "F":  {"name": "Fluorine",   "number": 9,   "mass": 18.998,  "category": "halogen"},
    "Ne": {"name": "Neon",       "number": 10,  "mass": 20.180,  "category": "noble gas"},
    "Na": {"name": "Sodium",     "number": 11,  "mass": 22.990,  "category": "alkali metal"},
    "Mg": {"name": "Magnesium",  "number": 12,  "mass": 24.305,  "category": "alkaline earth metal"},
    "Al": {"name": "Aluminium",  "number": 13,  "mass": 26.982,  "category": "post-transition metal"},
    "Si": {"name": "Silicon",    "number": 14,  "mass": 28.086,  "category": "metalloid"},
    "P":  {"name": "Phosphorus", "number": 15,  "mass": 30.974,  "category": "nonmetal"},
    "S":  {"name": "Sulphur",    "number": 16,  "mass": 32.065,  "category": "nonmetal"},
    "Cl": {"name": "Chlorine",   "number": 17,  "mass": 35.453,  "category": "halogen"},
    "Ar": {"name": "Argon",      "number": 18,  "mass": 39.948,  "category": "noble gas"},
    "K":  {"name": "Potassium",  "number": 19,  "mass": 39.098,  "category": "alkali metal"},
    "Ca": {"name": "Calcium",    "number": 20,  "mass": 40.078,  "category": "alkaline earth metal"},
    "Fe": {"name": "Iron",       "number": 26,  "mass": 55.845,  "category": "transition metal"},
    "Cu": {"name": "Copper",     "number": 29,  "mass": 63.546,  "category": "transition metal"},
    "Zn": {"name": "Zinc",       "number": 30,  "mass": 65.38,   "category": "transition metal"},
    "Ag": {"name": "Silver",     "number": 47,  "mass": 107.868, "category": "transition metal"},
    "Au": {"name": "Gold",       "number": 79,  "mass": 196.967, "category": "transition metal"},
    "Hg": {"name": "Mercury",    "number": 80,  "mass": 200.592, "category": "transition metal"},
    "Pb": {"name": "Lead",       "number": 82,  "mass": 207.2,   "category": "post-transition metal"},
    "U":  {"name": "Uranium",    "number": 92,  "mass": 238.029, "category": "actinide"},
}

# Build name lookup
_BY_NAME = {v["name"].lower(): k for k, v in _ELEMENTS.items()}


def get_element(query: str) -> str:
    """Look up an element by symbol or name."""
    query = query.strip()
    symbol = None

    # Try as symbol first
    if query.upper() in _ELEMENTS:
        symbol = query.upper()
    else:
        # Try as name
        symbol = _BY_NAME.get(query.lower())

    if not symbol:
        return f"Element '{query}' not found, sir. Try symbol like 'Fe' or name like 'Iron'."

    e = _ELEMENTS[symbol]
    return (
        f"{e['name']} (symbol: {symbol}, atomic number: {e['number']}, "
        f"atomic mass: {e['mass']}, category: {e['category']}), sir."
    )


def get_element_by_number(number: int) -> str:
    """Look up an element by atomic number."""
    for symbol, e in _ELEMENTS.items():
        if e["number"] == number:
            return get_element(symbol)
    return f"No element with atomic number {number} in database, sir."


def list_category(category: str) -> str:
    """List elements in a category."""
    cat     = category.lower()
    matches = [(s, e["name"]) for s, e in _ELEMENTS.items()
               if cat in e["category"].lower()]
    if not matches:
        return f"No elements found in category '{category}', sir."
    names = ", ".join(f"{name} ({sym})" for sym, name in matches)
    return f"{category.title()} elements: {names}, sir."
