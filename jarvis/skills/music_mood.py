"""
jarvis/skills/music_mood.py
Mood-based music recommendations — JARVIS suggests playlists
based on your mood, time of day, or activity.
Opens Spotify or YouTube Music with the right search.
"""
import webbrowser
import urllib.parse
import random

_MOOD_PLAYLISTS = {
    "focus": [
        "lofi hip hop beats to study to",
        "deep focus instrumental music",
        "brain food spotify",
        "coding music electronic",
        "Hans Zimmer concentration playlist",
    ],
    "energetic": [
        "power workout playlist",
        "high energy gym music 2024",
        "morning motivation songs",
        "epic running music",
        "heavy metal workout",
    ],
    "relaxed": [
        "chill vibes playlist",
        "evening wind down music",
        "acoustic relaxing songs",
        "jazz for relaxing",
        "ambient sleep music",
    ],
    "happy": [
        "feel good hits",
        "good mood songs playlist",
        "summer hits 2024",
        "dance pop happy songs",
        "upbeat indie playlist",
    ],
    "sad": [
        "sad songs playlist",
        "emotional music for crying",
        "heartbreak songs acoustic",
        "melancholy indie playlist",
    ],
    "productive": [
        "productivity music playlist",
        "binaural beats focus",
        "classical music for studying",
        "ambient techno work music",
    ],
    "iron man": [
        "AC DC back in black",
        "iron man black sabbath",
        "Tony Stark playlist rock",
        "superhero epic soundtrack",
    ],
}

_MOOD_RESPONSES = {
    "focus":      "Activating focus mode playlist, sir. Time to get to work.",
    "energetic":  "High energy playlist incoming, sir. Let's go.",
    "relaxed":    "Chill vibes selected, sir. Enjoy.",
    "happy":      "Good mood music, sir. The world approves.",
    "sad":        "I've got just the playlist, sir. Take your time.",
    "productive": "Productivity soundtrack engaged, sir.",
    "iron man":   "Classic Stark playlist, sir. AC/DC it is.",
}


def play_by_mood(mood: str, platform: str = "spotify") -> str:
    mood = mood.lower().strip()

    # Fuzzy match
    matched = None
    for key in _MOOD_PLAYLISTS:
        if key in mood or mood in key:
            matched = key
            break
    if not matched:
        moods = ", ".join(_MOOD_PLAYLISTS.keys())
        return f"I don't have a playlist for '{mood}', sir. Available moods: {moods}."

    query    = random.choice(_MOOD_PLAYLISTS[matched])
    response = _MOOD_RESPONSES.get(matched, f"Opening {matched} playlist, sir.")

    if platform == "youtube":
        url = f"https://music.youtube.com/search?q={urllib.parse.quote(query)}"
    else:
        url = f"https://open.spotify.com/search/{urllib.parse.quote(query)}"

    webbrowser.open(url)
    return response


def suggest_mood_music(time_hour: int | None = None) -> str:
    """Suggest a mood based on the time of day."""
    import datetime
    hour = time_hour or datetime.datetime.now().hour
    if 6 <= hour < 9:
        return "Based on the time, sir, I'd suggest an energetic morning playlist. Shall I open it?"
    elif 9 <= hour < 12:
        return "Morning work hours, sir. A focus or productive playlist would serve you well."
    elif 12 <= hour < 14:
        return "Lunchtime, sir. Perhaps something happy and upbeat?"
    elif 14 <= hour < 18:
        return "Afternoon slump incoming, sir. I recommend a productivity or focus playlist."
    elif 18 <= hour < 21:
        return "Evening, sir. A relaxed or chill playlist perhaps?"
    else:
        return "Late night, sir. Ambient or relaxed music would be appropriate."


def list_moods() -> str:
    moods = ", ".join(_MOOD_PLAYLISTS.keys())
    return f"Available music moods, sir: {moods}."
