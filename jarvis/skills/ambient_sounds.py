"""
jarvis/skills/ambient_sounds.py
Ambient sounds — JARVIS plays background soundscapes
for focus, sleep, or relaxation using online streams.
"""
import subprocess
import sys
import webbrowser

_SOUNDS = {
    "rain":        "https://rainymood.com",
    "coffee shop": "https://coffitivity.com",
    "ocean":       "https://www.youtube.com/watch?v=WHPEKLQID4U",
    "forest":      "https://www.youtube.com/watch?v=xNN7iTA57jM",
    "fire":        "https://www.youtube.com/watch?v=L_LUpnjgPso",
    "white noise": "https://www.youtube.com/watch?v=nMfPqeZjc2c",
    "brown noise": "https://www.youtube.com/watch?v=RqzGzwTY-6w",
    "thunderstorm":"https://www.youtube.com/watch?v=mPZkdNFkNps",
    "library":     "https://www.youtube.com/watch?v=3Ov-U9YoClE",
    "space":       "https://www.youtube.com/watch?v=H-iCZElJ8m0",
    "lofi":        "https://www.youtube.com/watch?v=jfKfPfyJRdk",
    "nature":      "https://www.youtube.com/watch?v=eKFTSSKCzWA",
}

_MOOD_MAP = {
    "focus":    ["lofi", "brown noise", "coffee shop", "library"],
    "sleep":    ["rain", "white noise", "ocean", "brown noise"],
    "relax":    ["nature", "forest", "ocean", "fire"],
    "energise": ["coffee shop", "lofi", "nature"],
}


def play_sound(sound_name: str) -> str:
    """Play an ambient sound."""
    sound_name = sound_name.lower().strip()
    url        = None

    for key, link in _SOUNDS.items():
        if sound_name in key or key in sound_name:
            url        = link
            sound_name = key
            break

    if not url:
        sounds = ", ".join(_SOUNDS.keys())
        return f"Sound '{sound_name}' not found, sir. Available: {sounds}."

    webbrowser.open(url)
    return f"Opening {sound_name} ambience, sir. Perfect for focus and flow."


def play_for_mood(mood: str) -> str:
    """Play ambient sound matching a mood."""
    import random
    mood   = mood.lower().strip()
    sounds = None

    for key, sound_list in _MOOD_MAP.items():
        if mood in key or key in mood:
            sounds = sound_list
            break

    if not sounds:
        moods = ", ".join(_MOOD_MAP.keys())
        return f"Mood '{mood}' not recognised, sir. Available: {moods}."

    chosen = random.choice(sounds)
    return play_sound(chosen)


def list_sounds() -> str:
    sounds = ", ".join(_SOUNDS.keys())
    return f"Available ambient sounds: {sounds}, sir."


def list_moods() -> str:
    moods = ", ".join(_MOOD_MAP.keys())
    return f"Ambient sound moods: {moods}, sir."
