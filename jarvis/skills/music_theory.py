"""Music theory — JARVIS explains chords, scales, and music concepts."""
import random

_SCALES = {
    "major": ["W","W","H","W","W","W","H"],
    "minor": ["W","H","W","W","H","W","W"],
    "pentatonic major": ["W","W","W+H","W","W+H"],
    "blues": ["W+H","W","H","H","W+H","W"],
}

_NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

_CHORDS = {
    "major": [0,4,7],
    "minor": [0,3,7],
    "dominant 7th": [0,4,7,10],
    "major 7th": [0,4,7,11],
    "minor 7th": [0,3,7,10],
    "diminished": [0,3,6],
    "augmented": [0,4,8],
}

_FACTS = [
    "A4 (concert pitch) is tuned to 440 Hz, sir.",
    "The circle of fifths shows all 12 major and minor keys, sir.",
    "An octave doubles the frequency — A3 is 220Hz, A4 is 440Hz, sir.",
    "Bach wrote over 1,000 compositions, including the Well-Tempered Clavier, sir.",
    "The blues scale is the foundation of rock, jazz, and pop music, sir.",
]

def get_chord(root: str, chord_type: str = "major") -> str:
    root = root.upper().strip()
    if root not in _NOTES:
        return f"'{root}' is not a valid note. Use C, C#, D, D#, E, F, F#, G, G#, A, A#, B, sir."
    intervals = _CHORDS.get(chord_type.lower())
    if not intervals:
        types = ", ".join(_CHORDS.keys())
        return f"Chord type not found. Available: {types}, sir."
    root_idx = _NOTES.index(root)
    notes    = [_NOTES[(root_idx + i) % 12] for i in intervals]
    return f"{root} {chord_type}: {' - '.join(notes)}, sir."

def get_scale(root: str, scale_type: str = "major") -> str:
    root = root.upper().strip()
    if root not in _NOTES:
        return f"'{root}' is not valid, sir."
    pattern = _SCALES.get(scale_type.lower())
    if not pattern:
        return f"Scale type not found. Available: {', '.join(_SCALES.keys())}, sir."
    idx   = _NOTES.index(root)
    notes = [root]
    step_map = {"W": 2, "H": 1, "W+H": 3}
    for step in pattern[:-1]:
        idx = (idx + step_map[step]) % 12
        notes.append(_NOTES[idx])
    return f"{root} {scale_type} scale: {' - '.join(notes)}, sir."

def get_music_fact() -> str:
    return random.choice(_FACTS)
