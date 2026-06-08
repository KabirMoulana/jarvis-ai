"""Natural disaster info — JARVIS explains disasters and safety procedures."""
_DISASTERS = {
    "earthquake": {
        "causes": "Earthquakes are caused by tectonic plate movement along fault lines, sir.",
        "safety": "DROP, COVER, HOLD ON. Get under a sturdy table. Stay away from windows. Don't run outside during shaking, sir.",
        "aftermath": "Check for gas leaks. Expect aftershocks. Stay away from damaged buildings, sir.",
    },
    "hurricane": {
        "causes": "Hurricanes form over warm ocean water when sea surface temps exceed 26°C, sir.",
        "safety": "Evacuate if ordered. Board up windows. Stock emergency supplies for 72 hours, sir.",
        "aftermath": "Avoid floodwater — it may be contaminated. Don't use generators indoors, sir.",
    },
    "tornado": {
        "causes": "Tornadoes form when warm moist air meets cold dry air, creating rotating thunderstorms, sir.",
        "safety": "Move to the lowest floor, interior room. Never shelter under a bridge or overpass, sir.",
        "aftermath": "Stay away from damaged power lines. Document damage for insurance, sir.",
    },
    "flood": {
        "causes": "Floods occur from heavy rainfall, storm surge, dam failure, or snowmelt, sir.",
        "safety": "Move to higher ground immediately. Never walk or drive through floodwater, sir.",
        "aftermath": "Don't return until authorities say it's safe. Avoid contact with floodwater, sir.",
    },
    "wildfire": {
        "causes": "Wildfires start from lightning, human activity, or sparks in dry conditions, sir.",
        "safety": "Evacuate early. Close all windows and doors. Leave lights on so you're visible in smoke, sir.",
        "aftermath": "Don't return until cleared. Beware of ash and debris — wear masks, sir.",
    },
}

def get_disaster_info(disaster: str) -> str:
    for key, info in _DISASTERS.items():
        if key in disaster.lower() or disaster.lower() in key:
            return (f"{key.title()} — {info['causes']} "
                    f"Safety: {info['safety']}")
    return f"Disaster type not found. Available: {', '.join(_DISASTERS.keys())}, sir."

def get_safety_tips(disaster: str) -> str:
    for key, info in _DISASTERS.items():
        if key in disaster.lower() or disaster.lower() in key:
            return f"{key.title()} safety, sir: {info['safety']}"
    return "Disaster type not found, sir."

def get_emergency_kit() -> str:
    return ("Emergency kit essentials, sir: Water (1 gallon per person per day for 3 days), "
            "non-perishable food, first aid kit, flashlight, batteries, "
            "whistle, dust masks, plastic sheeting, hand sanitiser, "
            "local maps, and copies of important documents.")
