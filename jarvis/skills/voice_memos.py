"""
jarvis/skills/voice_memos.py
Voice memos — JARVIS records short audio memos and plays them back.
Uses sounddevice + scipy for recording (no ffmpeg needed).
Falls back to a text memo if audio libs unavailable.
"""
import os
import json
from datetime import datetime

_MEMO_DIR  = os.path.expanduser("~/Documents/JarvisMemos")
_INDEX_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "memos_index.json")


def _load_index() -> list:
    try:
        if os.path.exists(_INDEX_FILE):
            with open(_INDEX_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save_index(data: list):
    os.makedirs(os.path.dirname(_INDEX_FILE), exist_ok=True)
    with open(_INDEX_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def record_memo(duration_secs: int = 10, label: str = "") -> str:
    """Record a voice memo."""
    os.makedirs(_MEMO_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"memo_{timestamp}.wav"
    path      = os.path.join(_MEMO_DIR, filename)

    try:
        import sounddevice as sd
        import scipy.io.wavfile as wav
        import numpy as np

        sample_rate = 44100
        print(f"[VoiceMemo] Recording for {duration_secs}s ...")
        recording = sd.rec(int(duration_secs * sample_rate),
                           samplerate=sample_rate, channels=1, dtype="int16")
        sd.wait()
        wav.write(path, sample_rate, recording)

        index = _load_index()
        index.append({"id": len(index)+1, "label": label or f"Memo {len(index)+1}",
                      "file": path, "created": timestamp})
        _save_index(index)
        return f"Voice memo recorded and saved as {filename}, sir."
    except ImportError:
        return _text_memo_fallback(label or "Voice memo", path)
    except Exception as e:
        return f"Recording failed: {e}"


def _text_memo_fallback(label: str, path: str) -> str:
    index = _load_index()
    index.append({"id": len(index)+1, "label": label, "file": None,
                  "created": datetime.now().isoformat()})
    _save_index(index)
    return f"Audio recording unavailable. Memo label saved as '{label}'. Install sounddevice for audio: pip install sounddevice scipy"


def play_memo(memo_id: int) -> str:
    """Play back a recorded memo."""
    index = _load_index()
    for m in index:
        if m["id"] == memo_id:
            path = m.get("file")
            if not path or not os.path.exists(path):
                return f"Audio file for memo {memo_id} not found, sir."
            try:
                import sounddevice as sd
                import scipy.io.wavfile as wav
                rate, data = wav.read(path)
                sd.play(data, rate)
                sd.wait()
                return f"Playing memo {memo_id}: '{m['label']}', sir."
            except Exception as e:
                return f"Playback failed: {e}"
    return f"Memo {memo_id} not found, sir."


def list_memos() -> str:
    index = _load_index()
    if not index:
        return "No voice memos saved, sir."
    recent = index[-5:]
    parts  = [f"{m['id']}. {m['label']} ({m['created'][:10]})" for m in reversed(recent)]
    return f"{len(index)} memo(s) saved. Recent: " + "; ".join(parts) + ", sir."


def delete_memo(memo_id: int) -> str:
    index = _load_index()
    for m in index:
        if m["id"] == memo_id:
            if m.get("file") and os.path.exists(m["file"]):
                os.remove(m["file"])
            index.remove(m)
            _save_index(index)
            return f"Memo {memo_id} deleted, sir."
    return f"Memo {memo_id} not found, sir."
