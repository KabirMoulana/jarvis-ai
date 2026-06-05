"""
jarvis/skills/smart_home_scenes.py
Smart home scenes — JARVIS activates preset home environments
like 'Movie Mode', 'Sleep Mode', 'Work Mode' with one command.
"""
from jarvis.skills.smart_home import turn_on, turn_off, set_brightness


_SCENES: dict[str, dict] = {
    "movie": {
        "description": "Dim lights, close blinds, optimise for viewing.",
        "actions": [
            ("living room light", "on",  20),
            ("bedroom light",     "off", 0),
            ("kitchen light",     "off", 0),
            ("tv",                "on",  100),
        ],
    },
    "sleep": {
        "description": "Turn off all lights, set bedroom to minimal.",
        "actions": [
            ("living room light", "off", 0),
            ("kitchen light",     "off", 0),
            ("bedroom light",     "on",  5),
            ("tv",                "off", 0),
        ],
    },
    "work": {
        "description": "Bright lights, minimal distractions.",
        "actions": [
            ("living room light", "on",  100),
            ("bedroom light",     "on",  80),
            ("tv",                "off", 0),
        ],
    },
    "party": {
        "description": "Full brightness, everything on.",
        "actions": [
            ("living room light", "on",  100),
            ("kitchen light",     "on",  100),
            ("bedroom light",     "on",  100),
        ],
    },
    "morning": {
        "description": "Gradual light increase to ease into the day.",
        "actions": [
            ("bedroom light",     "on",  30),
            ("kitchen light",     "on",  80),
            ("living room light", "on",  60),
        ],
    },
    "away": {
        "description": "All devices off for energy saving.",
        "actions": [
            ("living room light", "off", 0),
            ("bedroom light",     "off", 0),
            ("kitchen light",     "off", 0),
            ("tv",                "off", 0),
            ("fan",               "off", 0),
        ],
    },
}


def activate_scene(scene_name: str) -> str:
    """Activate a smart home scene."""
    scene_name = scene_name.lower().strip()
    scene      = None

    for key in _SCENES:
        if scene_name in key or key in scene_name:
            scene      = _SCENES[key]
            scene_name = key
            break

    if not scene:
        available = ", ".join(_SCENES.keys())
        return f"Scene '{scene_name}' not found, sir. Available: {available}."

    results = []
    for device, action, brightness in scene["actions"]:
        if action == "on" and brightness > 0:
            results.append(set_brightness(device, brightness))
        elif action == "on":
            results.append(turn_on(device))
        else:
            results.append(turn_off(device))

    return (
        f"Scene '{scene_name}' activated, sir. "
        f"{scene['description']} "
        f"{len(results)} device(s) updated."
    )


def list_scenes() -> str:
    parts = [f"{k}: {v['description']}" for k, v in _SCENES.items()]
    return "Available scenes, sir: " + " | ".join(parts) + "."


def create_scene(name: str, devices: list[tuple]) -> str:
    """Create a custom scene."""
    _SCENES[name.lower()] = {
        "description": f"Custom scene: {name}",
        "actions":     devices,
    }
    return f"Scene '{name}' created with {len(devices)} device action(s), sir."
