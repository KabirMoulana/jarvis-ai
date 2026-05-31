"""
jarvis/skills/spotify_control.py
Control Spotify via the spotipy library or AppleScript (macOS).
Supports: play, pause, next, previous, volume, current track info.

For full API control: pip install spotipy
Set env vars: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
"""
import sys
import subprocess
import os


# ── macOS AppleScript path (no API key needed) ────────────────────────────────

def _osascript(script: str) -> str:
    if sys.platform != "darwin":
        return ""
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip()


def _is_spotify_running() -> bool:
    if sys.platform == "darwin":
        result = _osascript('tell application "System Events" to (name of processes) contains "Spotify"')
        return result.lower() == "true"
    return False


def play_pause() -> str:
    if sys.platform == "darwin":
        _osascript('tell application "Spotify" to playpause')
        return "Toggling playback, sir."
    return "Spotify control via AppleScript is macOS-only."


def next_track() -> str:
    if sys.platform == "darwin":
        _osascript('tell application "Spotify" to next track')
        return "Skipping to the next track, sir."
    return "Spotify control is macOS-only."


def previous_track() -> str:
    if sys.platform == "darwin":
        _osascript('tell application "Spotify" to previous track')
        return "Going back a track, sir."
    return "Spotify control is macOS-only."


def get_current_track() -> str:
    if sys.platform == "darwin":
        track  = _osascript('tell application "Spotify" to name of current track')
        artist = _osascript('tell application "Spotify" to artist of current track')
        if track and artist:
            return f"Currently playing '{track}' by {artist}, sir."
        return "Nothing is playing on Spotify at the moment, sir."
    return "Spotify track info is macOS-only."


def set_spotify_volume(level: int) -> str:
    """Set Spotify volume 0-100."""
    level = max(0, min(100, level))
    if sys.platform == "darwin":
        _osascript(f'tell application "Spotify" to set sound volume to {level}')
        return f"Spotify volume set to {level} percent, sir."
    return "Spotify volume control is macOS-only."


def play_song(query: str) -> str:
    """
    Play a specific song by searching Spotify URI or opening a web search.
    Requires spotipy for full search — falls back to browser.
    """
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id     = os.getenv("SPOTIFY_CLIENT_ID", ""),
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", ""),
            redirect_uri  = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback"),
            scope         = "user-modify-playback-state user-read-playback-state",
        ))
        results = sp.search(q=query, type="track", limit=1)
        tracks  = results.get("tracks", {}).get("items", [])
        if not tracks:
            return f"No track found for '{query}', sir."
        uri  = tracks[0]["uri"]
        name = tracks[0]["name"]
        sp.start_playback(uris=[uri])
        return f"Playing '{name}' on Spotify, sir."
    except ImportError:
        import webbrowser, urllib.parse
        webbrowser.open(f"https://open.spotify.com/search/{urllib.parse.quote(query)}")
        return f"Opening Spotify search for '{query}', sir."
    except Exception as e:
        return f"Spotify play failed: {e}"
