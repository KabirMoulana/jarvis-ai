"""
jarvis/skills/voice_translator.py
Real-time voice translator — JARVIS listens in one language
and speaks the translation in another.
Combines STT + translation + TTS for live interpretation.
"""
import os


_SUPPORTED = {
    "spanish": "es", "french": "fr", "german": "de",
    "japanese": "ja", "chinese": "zh-cn", "arabic": "ar",
    "hindi": "hi", "portuguese": "pt", "russian": "ru",
    "korean": "ko", "italian": "it", "turkish": "tr",
}


def translate_speech(text: str, target_lang: str, source_lang: str = "en") -> str:
    """Translate text and return spoken translation."""
    from jarvis.skills.translate import translate
    result = translate(text, target_lang, source_lang)
    return result


def get_phrasebook(language: str) -> str:
    """Return essential travel phrases for a language."""
    phrases = {
        "spanish": [
            ("Hello", "Hola"), ("Thank you", "Gracias"),
            ("Where is the bathroom?", "¿Dónde está el baño?"),
            ("How much does this cost?", "¿Cuánto cuesta esto?"),
            ("I need help", "Necesito ayuda"),
            ("Do you speak English?", "¿Habla inglés?"),
        ],
        "french": [
            ("Hello", "Bonjour"), ("Thank you", "Merci"),
            ("Where is the bathroom?", "Où sont les toilettes?"),
            ("How much does this cost?", "Combien ça coûte?"),
            ("I need help", "J'ai besoin d'aide"),
            ("Do you speak English?", "Parlez-vous anglais?"),
        ],
        "japanese": [
            ("Hello", "Konnichiwa"), ("Thank you", "Arigatou gozaimasu"),
            ("Where is the bathroom?", "Toire wa doko desu ka?"),
            ("How much does this cost?", "Ikura desu ka?"),
            ("I need help", "Tasukete kudasai"),
            ("Do you speak English?", "Eigo wo hanasemasu ka?"),
        ],
        "arabic": [
            ("Hello", "Marhaba"), ("Thank you", "Shukran"),
            ("Where is the bathroom?", "Ayna al-hammam?"),
            ("How much does this cost?", "Bikam hatha?"),
            ("I need help", "Ahtaju musaada"),
        ],
    }
    lang = language.lower()
    for key, phrase_list in phrases.items():
        if lang in key or key in lang:
            parts = [f"{eng} = {trans}" for eng, trans in phrase_list]
            return f"{key.title()} phrasebook: " + " | ".join(parts) + ", sir."
    langs = ", ".join(phrases.keys())
    return f"Phrasebook not available for '{language}'. Available: {langs}, sir."


def language_code(name: str) -> str:
    """Get ISO language code for a language name."""
    name  = name.lower().strip()
    code  = _SUPPORTED.get(name, "unknown")
    if code == "unknown":
        return f"Language code for '{name}' not found, sir."
    return f"Language code for {name}: {code}, sir."
