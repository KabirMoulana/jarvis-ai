"""
jarvis/skills/vocabulary_builder.py
Vocabulary builder — JARVIS teaches you new words daily
with definitions, usage examples, and spaced repetition.
"""
import json
import os
import random
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "vocab.json")

_WORDS = [
    ("perspicacious", "Having a ready insight into things; shrewd.",
     "Her perspicacious analysis impressed the entire board."),
    ("sanguine", "Optimistic, especially in a difficult situation.",
     "Despite the setbacks, he remained sanguine about the outcome."),
    ("ephemeral", "Lasting for a very short time.",
     "The beauty of the sunset was ephemeral, gone within minutes."),
    ("laconic", "Using very few words; brief and concise.",
     "His laconic response — just 'no' — ended the debate."),
    ("mellifluous", "Sweet or musical; pleasant to hear.",
     "Her mellifluous voice filled the concert hall."),
    ("obfuscate", "To render obscure, unclear, or unintelligible.",
     "The report was designed to obfuscate rather than clarify."),
    ("tenacious", "Holding firmly to something; persistent.",
     "Her tenacious pursuit of excellence earned her the promotion."),
    ("equanimity", "Mental calmness in difficult situations.",
     "He faced the crisis with remarkable equanimity."),
    ("serendipity", "The occurrence of events by chance in a happy way.",
     "Finding that job was pure serendipity."),
    ("recalcitrant", "Having an obstinately uncooperative attitude.",
     "The recalcitrant student refused to follow any instruction."),
    ("loquacious", "Tending to talk a great deal; talkative.",
     "The loquacious host kept the audience entertained."),
    ("cogent", "Clear, logical, and convincing.",
     "She made a cogent argument for the new policy."),
    ("effervescent", "Vivacious and enthusiastic.",
     "Her effervescent personality lit up every room."),
    ("pernicious", "Having a harmful effect, especially in a subtle way.",
     "The pernicious influence of misinformation spread quickly."),
]


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"learned": [], "scores": {}}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2)


def word_of_day() -> str:
    """Return today's vocabulary word."""
    idx  = date.today().toordinal() % len(_WORDS)
    word, definition, example = _WORDS[idx]
    return (
        f"Vocabulary word of the day: '{word}'. "
        f"Definition: {definition} "
        f"Example: {example}, sir."
    )


def quiz_word() -> tuple[str, str]:
    """Return a random word for quizzing."""
    word, definition, _ = random.choice(_WORDS)
    return word, definition


def check_definition(word: str, given_definition: str) -> str:
    """Check if a definition is correct for a word."""
    for w, d, _ in _WORDS:
        if w.lower() == word.lower():
            key_terms = [t for t in d.lower().split() if len(t) > 4]
            given_terms = given_definition.lower().split()
            matches = sum(1 for t in key_terms if any(t in g for g in given_terms))
            score   = matches / max(len(key_terms), 1)
            if score >= 0.4:
                return f"Good definition, sir! The full definition: {d}"
            return f"Not quite, sir. '{w}' means: {d}"
    return f"Word '{word}' not in vocabulary list, sir."


def learn_word(word: str) -> str:
    """Mark a word as learned."""
    data = _load()
    if word.lower() not in data["learned"]:
        data["learned"].append(word.lower())
        _save(data)
    return f"'{word}' added to your learned vocabulary, sir."


def get_vocab_stats() -> str:
    data    = _load()
    learned = len(data["learned"])
    total   = len(_WORDS)
    return f"Vocabulary: {learned} words mastered out of {total} available, sir."
