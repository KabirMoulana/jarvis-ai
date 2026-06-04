"""
jarvis/skills/voice_clone.py
Voice synthesis upgrade — use ElevenLabs API for ultra-realistic
JARVIS voice, with pyttsx3 fallback.
Set ELEVENLABS_API_KEY in .env for premium voice.
"""
import os
import urllib.request
import urllib.error
import json
import tempfile

_API_KEY    = os.getenv("ELEVENLABS_API_KEY", "")
_VOICE_ID   = os.getenv("ELEVENLABS_VOICE_ID", "ErXwobaYiN019PkySvjV")  # Antoni — deep male
_API_URL    = "https://api.elevenlabs.io/v1/text-to-speech"
_MODEL      = "eleven_monolingual_v1"


def is_available() -> bool:
    return bool(_API_KEY)


def speak_elevenlabs(text: str) -> bool:
    """
    Synthesise speech using ElevenLabs API and play it.
    Returns True on success, False on failure.
    """
    if not _API_KEY:
        return False
    try:
        payload = json.dumps({
            "text": text,
            "model_id": _MODEL,
            "voice_settings": {
                "stability":        0.65,
                "similarity_boost": 0.80,
                "style":            0.20,
                "use_speaker_boost": True,
            }
        }).encode()

        req = urllib.request.Request(
            f"{_API_URL}/{_VOICE_ID}",
            data=payload,
            headers={
                "xi-api-key":   _API_KEY,
                "Content-Type": "application/json",
                "Accept":       "audio/mpeg",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            audio_data = resp.read()

        # Save to temp file and play
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(audio_data)
            tmp_path = f.name

        _play_audio(tmp_path)
        os.unlink(tmp_path)
        return True

    except Exception as e:
        print(f"[VoiceClone] ElevenLabs error: {e}")
        return False


def _play_audio(path: str):
    """Play audio file cross-platform."""
    import sys, subprocess
    if sys.platform == "darwin":
        subprocess.run(["afplay", path], check=True)
    elif sys.platform == "win32":
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME)
    else:
        subprocess.run(["mpg123", "-q", path], check=True)


def list_voices() -> str:
    """List available ElevenLabs voices."""
    if not _API_KEY:
        return "ElevenLabs API key not set, sir. Add ELEVENLABS_API_KEY to your .env file."
    try:
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": _API_KEY}
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data   = json.loads(resp.read())
        voices = [v["name"] for v in data.get("voices", [])]
        return f"Available voices: {', '.join(voices[:8])}, sir."
    except Exception as e:
        return f"Could not fetch voices: {e}"


def set_voice(voice_id: str) -> str:
    global _VOICE_ID
    _VOICE_ID = voice_id
    return f"Voice set to {voice_id}, sir."


def get_status() -> str:
    if _API_KEY:
        return f"ElevenLabs voice active, sir. Voice ID: {_VOICE_ID}."
    return "ElevenLabs not configured. Using pyttsx3 fallback. Set ELEVENLABS_API_KEY in .env to upgrade."
