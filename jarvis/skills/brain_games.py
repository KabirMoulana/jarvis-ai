"""
jarvis/skills/brain_games.py
Brain training games — JARVIS challenges your memory,
logic, and pattern recognition. 
Games: memory sequence, word scramble, number guessing.
"""
import random
import time

_memory_game: dict   = {}
_number_game: dict   = {}


# ── Memory sequence ────────────────────────────────────────────────────────────
def start_memory_game(length: int = 5) -> str:
    global _memory_game
    sequence = [random.randint(0, 9) for _ in range(length)]
    _memory_game = {"sequence": sequence, "shown": True}
    seq_str = " ".join(map(str, sequence))
    return (
        f"Memory game! Remember this sequence, sir: {seq_str}. "
        f"I'll ask you to repeat it in 5 seconds."
    )


def check_memory_answer(answer: str) -> str:
    if not _memory_game.get("shown"):
        return "No active memory game, sir."
    try:
        given    = list(map(int, answer.strip().split()))
        correct  = _memory_game["sequence"]
        if given == correct:
            return f"Perfect recall, sir! The sequence was {' '.join(map(str, correct))}."
        else:
            wrong = sum(1 for a, b in zip(given, correct) if a != b)
            return f"Close, sir. The sequence was {' '.join(map(str, correct))}. You got {len(correct)-wrong}/{len(correct)} correct."
    except ValueError:
        return "Please repeat the numbers separated by spaces, sir."


# ── Number guessing ────────────────────────────────────────────────────────────
def start_guessing_game(max_num: int = 100) -> str:
    global _number_game
    target  = random.randint(1, max_num)
    _number_game = {"target": target, "max": max_num, "attempts": 0, "active": True}
    return f"I'm thinking of a number between 1 and {max_num}, sir. Take a guess."


def make_guess(guess: str) -> str:
    if not _number_game.get("active"):
        return "No active guessing game, sir."
    try:
        n = int(guess.strip())
    except ValueError:
        return "Please guess a number, sir."
    target = _number_game["target"]
    _number_game["attempts"] += 1
    attempts = _number_game["attempts"]
    if n == target:
        _number_game["active"] = False
        rating = "incredible" if attempts <= 5 else "good" if attempts <= 8 else "not bad"
        return f"Correct, sir! The number was {target}. You got it in {attempts} attempt(s) — {rating}!"
    hint = "Too high, sir." if n > target else "Too low, sir."
    return f"{hint} {attempts} attempt(s) so far."


# ── Word scramble ──────────────────────────────────────────────────────────────
_WORD_BANK = [
    "jarvis", "reactor", "avenger", "quantum", "vibranium", "algorithm",
    "intelligence", "processor", "hologram", "innovation", "technology",
    "encryption", "satellite", "prototype", "engineering"
]

_scramble_game: dict = {}


def start_word_scramble() -> str:
    global _scramble_game
    word    = random.choice(_WORD_BANK)
    letters = list(word)
    random.shuffle(letters)
    while "".join(letters) == word:
        random.shuffle(letters)
    scrambled = " ".join(letters).upper()
    _scramble_game = {"word": word, "active": True}
    return f"Unscramble this word, sir: {scrambled}"


def check_scramble_answer(answer: str) -> str:
    if not _scramble_game.get("active"):
        return "No active word scramble, sir."
    correct = _scramble_game["word"]
    if answer.lower().strip() == correct:
        _scramble_game["active"] = False
        return f"Correct, sir! The word was '{correct}'."
    return f"Not quite, sir. Give it another try."


def scramble_hint() -> str:
    if not _scramble_game.get("active"):
        return "No active word scramble, sir."
    word = _scramble_game["word"]
    hint = word[0] + "_" * (len(word) - 2) + word[-1]
    return f"Hint: the word starts with '{word[0]}' and ends with '{word[-1]}' — {hint}, sir."
