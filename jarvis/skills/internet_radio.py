"""
jarvis/skills/internet_radio.py
Internet radio — JARVIS plays live radio streams.
Opens streams in the default media player or browser.
No API key required.
"""
import subprocess
import sys
import webbrowser


_STATIONS = {
    "bbc radio 1":    "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
    "bbc radio 2":    "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two",
    "bbc radio 4":    "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
    "bbc world service": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "jazz fm":        "http://listen.jazzmusiconline.net:8080/",
    "classical":      "http://live-radio01.mediahubaustralia.com/2ABCclassical/mp3/",
    "lofi":           "http://lofi.stream.laut.fm/lofi",
    "chillhop":       "http://chillhop.out.airtime.pro:8000/chillhop_a",
    "news":           "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
    "talk radio":     "http://stream.live.vc.bbcmedia.co.uk/bbc_5_live_sports_extra",
}


def play_station(name: str) -> str:
    """Play a radio station by name."""
    name = name.lower().strip()
    url  = None

    for key, stream_url in _STATIONS.items():
        if name in key or key in name:
            url  = stream_url
            name = key
            break

    if not url:
        stations = ", ".join(_STATIONS.keys())
        return f"Station '{name}' not found, sir. Available: {stations}."

    # Try mpv/vlc first, fallback to browser
    players = ["mpv", "vlc", "ffplay"]
    for player in players:
        try:
            result = subprocess.run(["which", player], capture_output=True)
            if result.returncode == 0:
                subprocess.Popen([player, url],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                return f"Playing {name.title()}, sir."
        except Exception:
            pass

    # Browser fallback
    webbrowser.open(url)
    return f"Opening {name.title()} in your browser, sir. Install mpv for better audio."


def list_stations() -> str:
    """List all available radio stations."""
    names = ", ".join(k.title() for k in _STATIONS.keys())
    return f"Available radio stations: {names}, sir."


def stop_radio() -> str:
    """Stop any playing radio streams."""
    for player in ["mpv", "vlc", "ffplay"]:
        try:
            subprocess.run(["pkill", "-f", player], capture_output=True)
        except Exception:
            pass
    return "Radio stopped, sir."
