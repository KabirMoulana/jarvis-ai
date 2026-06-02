"""
jarvis/skills/smart_home.py
Smart home control — JARVIS-style home automation.
Supports: Home Assistant (local), basic GPIO (Raspberry Pi),
and a simulator mode for development.
"""
import os
import urllib.request
import urllib.error
import json

_HA_URL   = os.getenv("HOME_ASSISTANT_URL", "http://homeassistant.local:8123")
_HA_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN", "")
_SIM_MODE = not bool(_HA_TOKEN)

# Simulated device state for development / demo
_SIM_DEVICES: dict[str, dict] = {
    "living room light":  {"state": "off", "entity": "light.living_room"},
    "bedroom light":      {"state": "off", "entity": "light.bedroom"},
    "kitchen light":      {"state": "off", "entity": "light.kitchen"},
    "fan":                {"state": "off", "entity": "switch.fan"},
    "tv":                 {"state": "off", "entity": "media_player.tv"},
    "ac":                 {"state": "off", "entity": "climate.ac"},
}


def turn_on(device: str) -> str:
    return _control(device, "on")


def turn_off(device: str) -> str:
    return _control(device, "off")


def toggle(device: str) -> str:
    key = _find_device(device)
    if key and _SIM_MODE:
        current = _SIM_DEVICES[key]["state"]
        return _control(device, "off" if current == "on" else "on")
    return _control(device, "toggle")


def device_status(device: str = "") -> str:
    if _SIM_MODE:
        if device:
            key = _find_device(device)
            if key:
                state = _SIM_DEVICES[key]["state"]
                return f"{key.capitalize()} is currently {state}, sir."
            return f"Device '{device}' not found, sir."
        lines = [f"{k}: {v['state']}" for k, v in _SIM_DEVICES.items()]
        return "Home status — " + ", ".join(lines) + "."

    return _ha_request("GET", "/api/states", None)


def set_brightness(device: str, level: int) -> str:
    """Set light brightness 0-100%."""
    level = max(0, min(100, level))
    brightness = int(level * 2.55)  # convert to 0-255
    if _SIM_MODE:
        key = _find_device(device)
        if key:
            _SIM_DEVICES[key]["state"] = f"on (brightness {level}%)"
            return f"{key.capitalize()} brightness set to {level} percent, sir."
        return f"Device '{device}' not found in simulation, sir."
    entity = _get_entity(device)
    payload = {"entity_id": entity, "brightness": brightness}
    return _ha_request("POST", "/api/services/light/turn_on", payload)


def _control(device: str, action: str) -> str:
    key = _find_device(device)
    if _SIM_MODE:
        if key:
            _SIM_DEVICES[key]["state"] = action
            verb = "turned on" if action == "on" else "turned off"
            return f"{key.capitalize()} {verb}, sir."
        return f"Device '{device}' not found in simulation, sir."

    entity  = _get_entity(device)
    domain  = entity.split(".")[0]
    service = f"turn_{action}" if action in ("on", "off") else "toggle"
    payload = {"entity_id": entity}
    return _ha_request("POST", f"/api/services/{domain}/{service}", payload)


def _find_device(name: str) -> str | None:
    name = name.lower().strip()
    for key in _SIM_DEVICES:
        if name in key or key in name:
            return key
    return None


def _get_entity(device: str) -> str:
    key = _find_device(device)
    if key:
        return _SIM_DEVICES[key]["entity"]
    return f"switch.{device.lower().replace(' ', '_')}"


def _ha_request(method: str, path: str, payload: dict | None) -> str:
    try:
        url  = _HA_URL + path
        data = json.dumps(payload).encode() if payload else None
        req  = urllib.request.Request(
            url, data=data, method=method,
            headers={
                "Authorization": f"Bearer {_HA_TOKEN}",
                "Content-Type":  "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return f"Command sent successfully, sir."
    except urllib.error.URLError:
        return "Home Assistant not reachable, sir. Check your local network."
    except Exception as e:
        return f"Smart home error: {e}"
