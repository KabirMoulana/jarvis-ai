"""
jarvis/skills/dictionary.py
Dictionary and thesaurus — word definitions, synonyms,
antonyms and pronunciation via free APIs. No key required.
"""
import urllib.request
import urllib.parse
import json


_FREE_DICT = "https://api.dictionaryapi.dev/api/v2/entries/en"


def define(word: str) -> str:
    """Look up the definition of a word."""
    word = word.strip().lower()
    try:
        url = f"{_FREE_DICT}/{urllib.parse.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())

        entry    = data[0]
        meanings = entry.get("meanings", [])
        if not meanings:
            return f"No definition found for '{word}', sir."

        parts = []
        for meaning in meanings[:2]:
            pos  = meaning.get("partOfSpeech", "")
            defs = meaning.get("definitions", [])
            if defs:
                parts.append(f"{pos}: {defs[0]['definition']}")
                example = defs[0].get("example", "")
                if example:
                    parts.append(f"Example: {example}")

        phonetic = entry.get("phonetic", "")
        intro    = f"'{word}'"
        if phonetic:
            intro += f" ({phonetic})"

        return f"{intro} — " + ". ".join(parts) + "."
    except Exception:
        return f"No definition found for '{word}', sir. It may be a proper noun or uncommon term."


def synonyms(word: str) -> str:
    """Get synonyms for a word."""
    word = word.strip().lower()
    try:
        url = f"{_FREE_DICT}/{urllib.parse.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())

        syns = []
        for entry in data:
            for meaning in entry.get("meanings", []):
                syns.extend(meaning.get("synonyms", []))
                for defn in meaning.get("definitions", []):
                    syns.extend(defn.get("synonyms", []))

        syns = list(dict.fromkeys(syns))[:8]
        if not syns:
            return f"No synonyms found for '{word}', sir."
        return f"Synonyms for '{word}': {', '.join(syns)}, sir."
    except Exception:
        return f"Could not find synonyms for '{word}', sir."


def antonyms(word: str) -> str:
    """Get antonyms for a word."""
    word = word.strip().lower()
    try:
        url = f"{_FREE_DICT}/{urllib.parse.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())

        ants = []
        for entry in data:
            for meaning in entry.get("meanings", []):
                ants.extend(meaning.get("antonyms", []))
                for defn in meaning.get("definitions", []):
                    ants.extend(defn.get("antonyms", []))

        ants = list(dict.fromkeys(ants))[:6]
        if not ants:
            return f"No antonyms found for '{word}', sir."
        return f"Antonyms for '{word}': {', '.join(ants)}, sir."
    except Exception:
        return f"Could not find antonyms for '{word}', sir."


def word_of_the_day() -> str:
    """Return a curated word of the day."""
    from datetime import date
    words = [
        ("ephemeral",  "lasting for a very short time"),
        ("perspicacious", "having a ready insight; shrewd"),
        ("sonder",     "the realisation that each passerby has a life as complex as your own"),
        ("laconic",    "using very few words"),
        ("serendipity","the occurrence of events by chance in a happy way"),
        ("mellifluous","having a pleasant, sweet sound"),
        ("ineffable",  "too great to be expressed in words"),
        ("cogent",     "clear, logical and convincing"),
        ("quixotic",   "exceedingly idealistic; unrealistic"),
        ("luminous",   "full of or shedding light; bright"),
        ("tenacious",  "holding firmly; persistent"),
        ("perspicuous","clearly expressed; easy to understand"),
    ]
    idx  = date.today().toordinal() % len(words)
    word, definition = words[idx]
    return f"Word of the day, sir: '{word}' — {definition}."
