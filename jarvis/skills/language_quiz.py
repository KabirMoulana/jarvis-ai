"""
jarvis/skills/language_quiz.py
Language learning quiz — JARVIS quizzes you on vocabulary.
Supports multiple languages with a spaced-repetition-lite scoring system.
"""
import random
import json
import os
from datetime import datetime

_SCORE_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "quiz_scores.json")

_VOCAB: dict[str, list[tuple[str, str]]] = {
    "spanish": [
        ("hello", "hola"), ("goodbye", "adiós"), ("thank you", "gracias"),
        ("please", "por favor"), ("yes", "sí"), ("no", "no"),
        ("water", "agua"), ("food", "comida"), ("house", "casa"),
        ("book", "libro"), ("time", "tiempo"), ("love", "amor"),
    ],
    "french": [
        ("hello", "bonjour"), ("goodbye", "au revoir"), ("thank you", "merci"),
        ("please", "s'il vous plaît"), ("yes", "oui"), ("no", "non"),
        ("water", "eau"), ("food", "nourriture"), ("house", "maison"),
        ("book", "livre"), ("time", "temps"), ("love", "amour"),
    ],
    "japanese": [
        ("hello", "konnichiwa"), ("goodbye", "sayonara"), ("thank you", "arigatou"),
        ("please", "onegaishimasu"), ("yes", "hai"), ("no", "iie"),
        ("water", "mizu"), ("food", "tabemono"), ("house", "ie"),
        ("book", "hon"), ("time", "jikan"), ("love", "ai"),
    ],
    "arabic": [
        ("hello", "marhaba"), ("goodbye", "ma'a salama"), ("thank you", "shukran"),
        ("please", "min fadlak"), ("yes", "naam"), ("no", "la"),
        ("water", "maa"), ("food", "akl"), ("house", "bayt"),
    ],
}

_current_question: dict = {}


def start_quiz(language: str = "spanish") -> str:
    global _current_question
    lang  = language.lower().strip()
    vocab = _VOCAB.get(lang)
    if not vocab:
        langs = ", ".join(_VOCAB.keys())
        return f"Language '{language}' not available, sir. Try: {langs}."

    english, translation = random.choice(vocab)
    _current_question = {
        "language":    lang,
        "english":     english,
        "translation": translation,
        "asked_at":    datetime.now().isoformat(),
    }
    return f"Quiz time, sir. How do you say '{english}' in {language}?"


def check_answer(user_answer: str) -> str:
    if not _current_question:
        return "No active quiz question, sir. Say 'quiz me in Spanish' to start."

    correct = _current_question["translation"].lower().strip()
    given   = user_answer.lower().strip()
    lang    = _current_question["language"]
    english = _current_question["english"]

    _update_score(lang, given == correct)

    if given == correct:
        return (
            f"Correct, sir! '{english}' in {lang} is indeed '{correct}'. "
            f"Shall we continue?"
        )
    return (
        f"Not quite, sir. '{english}' in {lang} is '{correct}', not '{given}'. "
        f"Keep practising."
    )


def get_score(language: str = "") -> str:
    scores = _load_scores()
    if language:
        lang = language.lower()
        s    = scores.get(lang, {"correct": 0, "total": 0})
        pct  = int(s["correct"] / s["total"] * 100) if s["total"] else 0
        return f"{lang.capitalize()} quiz score: {s['correct']}/{s['total']} ({pct}%), sir."
    if not scores:
        return "No quiz scores recorded yet, sir."
    parts = []
    for lang, s in scores.items():
        pct = int(s["correct"] / s["total"] * 100) if s["total"] else 0
        parts.append(f"{lang}: {pct}%")
    return "Quiz scores — " + ", ".join(parts) + ", sir."


def _update_score(language: str, correct: bool):
    scores = _load_scores()
    if language not in scores:
        scores[language] = {"correct": 0, "total": 0}
    scores[language]["total"]   += 1
    scores[language]["correct"] += int(correct)
    _save_scores(scores)


def _load_scores() -> dict:
    try:
        if os.path.exists(_SCORE_FILE):
            with open(_SCORE_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_scores(scores: dict):
    os.makedirs(os.path.dirname(_SCORE_FILE), exist_ok=True)
    with open(_SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=2)
