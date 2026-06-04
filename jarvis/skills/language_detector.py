"""
jarvis/skills/language_detector.py
Language detection — JARVIS identifies what language text is in.
Uses langdetect library with a manual fallback based on character sets.
"""


def detect_language(text: str) -> str:
    """Detect the language of a given text."""
    text = text.strip()
    if not text:
        return "No text provided, sir."

    # Try langdetect first
    try:
        from langdetect import detect, detect_langs
        langs   = detect_langs(text)
        top     = langs[0]
        lang    = _code_to_name(str(top.lang))
        conf    = top.prob
        return f"That appears to be {lang}, sir. Confidence: {conf:.0%}."
    except ImportError:
        pass
    except Exception:
        pass

    # Manual fallback using Unicode ranges
    return _manual_detect(text)


def _manual_detect(text: str) -> str:
    """Basic language detection via Unicode character ranges."""
    counts = {
        "Arabic":   sum(1 for c in text if "\u0600" <= c <= "\u06FF"),
        "Chinese":  sum(1 for c in text if "\u4E00" <= c <= "\u9FFF"),
        "Japanese": sum(1 for c in text if "\u3040" <= c <= "\u309F" or "\u30A0" <= c <= "\u30FF"),
        "Korean":   sum(1 for c in text if "\uAC00" <= c <= "\uD7AF"),
        "Cyrillic": sum(1 for c in text if "\u0400" <= c <= "\u04FF"),
        "Greek":    sum(1 for c in text if "\u0370" <= c <= "\u03FF"),
        "Hindi":    sum(1 for c in text if "\u0900" <= c <= "\u097F"),
        "Tamil":    sum(1 for c in text if "\u0B80" <= c <= "\u0BFF"),
    }
    detected = max(counts, key=counts.get)
    if counts[detected] > 0:
        return f"That appears to contain {detected} script, sir."
    return "The text appears to be in a Latin-based language, sir. Install langdetect for precise detection."


def _code_to_name(code: str) -> str:
    codes = {
        "en": "English", "fr": "French", "de": "German", "es": "Spanish",
        "it": "Italian", "pt": "Portuguese", "nl": "Dutch", "ru": "Russian",
        "ar": "Arabic", "zh-cn": "Chinese", "zh-tw": "Chinese (Traditional)",
        "ja": "Japanese", "ko": "Korean", "hi": "Hindi", "tr": "Turkish",
        "pl": "Polish", "sv": "Swedish", "no": "Norwegian", "da": "Danish",
        "fi": "Finnish", "cs": "Czech", "ro": "Romanian", "hu": "Hungarian",
        "uk": "Ukrainian", "th": "Thai", "vi": "Vietnamese", "id": "Indonesian",
        "ms": "Malay", "ta": "Tamil", "ur": "Urdu", "fa": "Persian",
    }
    return codes.get(code.lower(), code.upper())


def is_english(text: str) -> bool:
    """Quick check if text is likely English."""
    try:
        from langdetect import detect
        return detect(text) == "en"
    except Exception:
        return True  # Assume English on failure
