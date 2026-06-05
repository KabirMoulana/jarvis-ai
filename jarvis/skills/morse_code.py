"""
jarvis/skills/morse_code.py
Morse code translator — JARVIS encodes and decodes morse code.
Also plays it as audio beeps.
"""
import time
import threading

_TO_MORSE = {
    'A':'.-',   'B':'-...', 'C':'-.-.', 'D':'-..',  'E':'.',
    'F':'..-.', 'G':'--.',  'H':'....', 'I':'..',   'J':'.---',
    'K':'-.-',  'L':'.-..', 'M':'--',   'N':'-.',   'O':'---',
    'P':'.--.', 'Q':'--.-', 'R':'.-.',  'S':'...',  'T':'-',
    'U':'..-',  'V':'...-', 'W':'.--',  'X':'-..-', 'Y':'-.--',
    'Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
    '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    '.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--',
    '/':'-..-.', ' ': '/',
}

_FROM_MORSE = {v: k for k, v in _TO_MORSE.items()}


def encode(text: str) -> str:
    """Convert text to morse code."""
    text  = text.upper()
    morse = " ".join(_TO_MORSE.get(c, c) for c in text)
    return f"Morse code: {morse}, sir."


def decode(morse: str) -> str:
    """Convert morse code to text."""
    words  = morse.strip().split(" / ")
    result = []
    for word in words:
        chars = word.split()
        result.append("".join(_FROM_MORSE.get(c, "?") for c in chars))
    decoded = " ".join(result)
    return f"Decoded: {decoded}, sir."


def play_morse(text: str, callback=None) -> str:
    """Play morse code as audio beeps."""
    text  = text.upper()
    morse = " ".join(_TO_MORSE.get(c, "") for c in text if c in _TO_MORSE)

    def _beep():
        try:
            import sys
            for symbol in morse:
                if symbol == ".":
                    sys.stdout.write("\a"); sys.stdout.flush()
                    time.sleep(0.1)
                elif symbol == "-":
                    sys.stdout.write("\a"); sys.stdout.flush()
                    time.sleep(0.3)
                elif symbol == " ":
                    time.sleep(0.1)
                time.sleep(0.05)
        except Exception:
            pass

    t = threading.Thread(target=_beep, daemon=True)
    t.start()
    return f"Playing morse code for '{text}', sir. {morse}"


def is_valid_morse(morse: str) -> str:
    """Check if a string is valid morse code."""
    valid_chars = set(".- /")
    invalid     = [c for c in morse if c not in valid_chars]
    if invalid:
        return f"Invalid morse code characters found: {''.join(set(invalid))}, sir."
    return "Valid morse code, sir."
