"""
jarvis/skills/study_helper.py
Study helper — JARVIS assists with studying via flashcards,
Pomodoro study sessions, and quiz generation.
"""
import json
import os
import random
from datetime import datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "flashcards.json")


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(cards: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(cards, f, indent=2)


def add_flashcard(question: str, answer: str, deck: str = "general") -> str:
    cards = _load()
    card  = {
        "id":       len(cards) + 1,
        "deck":     deck.lower(),
        "question": question.strip(),
        "answer":   answer.strip(),
        "correct":  0,
        "attempts": 0,
    }
    cards.append(card)
    _save(cards)
    return f"Flashcard added to '{deck}' deck, sir. Total cards: {len(cards)}."


def get_flashcard(deck: str = "") -> str:
    cards = _load()
    if deck:
        cards = [c for c in cards if deck.lower() in c["deck"]]
    if not cards:
        return "No flashcards found, sir. Add some with 'add flashcard [question] answer [answer]'."
    # Prioritise cards with lower accuracy
    cards.sort(key=lambda c: (c["correct"] / c["attempts"]) if c["attempts"] else 0)
    card = cards[0]
    return f"Flashcard #{card['id']} ({card['deck']}): {card['question']}"


def answer_flashcard(card_id: int, user_answer: str) -> str:
    cards = _load()
    for card in cards:
        if card["id"] == card_id:
            card["attempts"] += 1
            correct = user_answer.lower().strip() in card["answer"].lower()
            if correct:
                card["correct"] += 1
            _save(cards)
            acc = int(card["correct"] / card["attempts"] * 100)
            if correct:
                return f"Correct, sir! The answer is '{card['answer']}'. Accuracy: {acc}%."
            return f"Not quite, sir. The answer is '{card['answer']}'. Accuracy: {acc}%."
    return f"Card {card_id} not found, sir."


def list_decks() -> str:
    cards = _load()
    if not cards:
        return "No flashcards yet, sir."
    decks = {}
    for c in cards:
        decks[c["deck"]] = decks.get(c["deck"], 0) + 1
    parts = [f"{k} ({v} cards)" for k, v in decks.items()]
    return "Study decks: " + ", ".join(parts) + ", sir."


def study_stats() -> str:
    cards = _load()
    if not cards:
        return "No flashcards yet, sir."
    attempted = [c for c in cards if c["attempts"] > 0]
    if not attempted:
        return f"You have {len(cards)} flashcard(s) but none studied yet, sir."
    avg_acc = sum(c["correct"] / c["attempts"] for c in attempted) / len(attempted) * 100
    return (
        f"Study stats, sir: {len(cards)} total cards. "
        f"{len(attempted)} studied. Average accuracy: {avg_acc:.0f}%."
    )
