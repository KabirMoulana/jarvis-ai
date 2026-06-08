"""Language facts — JARVIS shares fascinating linguistics facts."""
import random

_FACTS = [
    "There are approximately 7,000 languages spoken in the world today, sir.",
    "Mandarin Chinese is the most spoken native language with over 900 million speakers, sir.",
    "English borrows about 30% of its vocabulary from French, sir.",
    "The language with the most words is English, with over 1 million words, sir.",
    "Hawaiian has only 13 letters in its alphabet, sir.",
    "The Pirahã language of the Amazon has no words for numbers — only concepts of 'few' and 'many', sir.",
    "Russian has no word for 'the' or 'a' — definite articles don't exist, sir.",
    "The word 'set' has the most meanings in English — over 430 definitions, sir.",
    "Sanskrit is considered the oldest written language still in use, sir.",
    "The Silbo Gomero is a whistled language used in the Canary Islands, sir.",
    "Finnish has 15 grammatical cases compared to English's 3, sir.",
    "The language with the longest alphabet is Khmer with 74 letters, sir.",
    "A 'pangram' is a sentence using every letter of the alphabet — 'The quick brown fox jumps over the lazy dog', sir.",
    "The word 'goodbye' is a contraction of 'God be with ye', sir.",
    "Shakespeare invented over 1,700 words including 'bedroom', 'lonely', and 'generous', sir.",
]

_LINGUISTIC_CONCEPTS = {
    "phoneme":   "The smallest unit of sound in a language. English has about 44 phonemes, sir.",
    "morpheme":  "The smallest unit of meaning. 'Unhappy' has 2: 'un' + 'happy', sir.",
    "syntax":    "The rules that govern sentence structure in a language, sir.",
    "semantics": "The study of meaning in language — what words and sentences mean, sir.",
    "etymology": "The study of the origin and history of words, sir.",
    "dialect":   "A regional or social variety of a language with distinct vocabulary and grammar, sir.",
    "lingua franca": "A language used for communication between people with different native languages, sir.",
}

def get_fact() -> str:
    return random.choice(_FACTS)

def explain_concept(concept: str) -> str:
    for key, desc in _LINGUISTIC_CONCEPTS.items():
        if key in concept.lower() or concept.lower() in key:
            return desc
    return f"Linguistic concept '{concept}' not found, sir."

def get_daily_fact() -> str:
    from datetime import date
    idx = date.today().toordinal() % len(_FACTS)
    return _FACTS[idx]
