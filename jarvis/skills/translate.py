"""
jarvis/skills/translate.py
Language translation — uses Google Translate (no API key via googletrans)
or falls back to MyMemory free API.
"""
import urllib.request
import urllib.parse
import json


_LANG_CODES = {
    "arabic": "ar", "chinese": "zh-cn", "mandarin": "zh-cn",
    "french": "fr", "german": "de", "hindi": "hi",
    "italian": "it", "japanese": "ja", "korean": "ko",
    "portuguese": "pt", "russian": "ru", "spanish": "es",
    "tamil": "ta", "turkish": "tr", "urdu": "ur",
    "english": "en", "dutch": "nl", "greek": "el",
    "polish": "pl", "swedish": "sv",
}


def translate(text: str, target_lang: str, source_lang: str = "auto") -> str:
    lang_code = _LANG_CODES.get(target_lang.lower(), target_lang.lower())

    # Try googletrans first
    try:
        from googletrans import Translator
        t      = Translator()
        result = t.translate(text, dest=lang_code, src=source_lang)
        return (
            f"Translation to {target_lang}: {result.text}. "
            f"Pronunciation: {result.pronunciation or ''}."
        ).strip()
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: MyMemory free API
    return _mymemory_translate(text, lang_code, source_lang)


def _mymemory_translate(text: str, lang_code: str, source: str = "auto") -> str:
    try:
        if source == "auto":
            source = "en"
        pair    = f"{source}|{lang_code}"
        encoded = urllib.parse.quote(text)
        url     = f"https://api.mymemory.translated.net/get?q={encoded}&langpair={pair}"
        req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        translated = data["responseData"]["translatedText"]
        return f"Translation: {translated}."
    except Exception as e:
        return f"Translation failed, sir: {e}"


def detect_language(text: str) -> str:
    try:
        from googletrans import Translator
        t      = Translator()
        result = t.detect(text)
        return f"That appears to be {result.lang}, sir. Confidence: {result.confidence:.0%}."
    except ImportError:
        return "Language detection requires: pip install googletrans==4.0.0rc1"
    except Exception as e:
        return f"Detection failed: {e}"


def list_languages() -> str:
    langs = ", ".join(sorted(_LANG_CODES.keys()))
    return f"Supported languages: {langs}."
