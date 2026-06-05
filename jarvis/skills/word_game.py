"""
jarvis/skills/word_game.py
Word games — JARVIS plays word association, 20 questions,
and story builder with you.
"""
import random

_WORD_ASSOCIATIONS = {
    "iron": ["steel", "strong", "press", "man", "ore"],
    "star": ["space", "light", "wars", "fish", "bright"],
    "fire": ["hot", "burn", "red", "flame", "truck"],
    "tech": ["code", "digital", "smart", "future", "AI"],
    "brain": ["think", "smart", "mind", "neural", "head"],
}

_20Q_OBJECTS = [
    {"object": "the Eiffel Tower", "animal": False, "vegetable": False,
     "bigger": True, "metal": True, "France": True},
    {"object": "a smartphone", "animal": False, "vegetable": False,
     "bigger": False, "electronic": True, "portable": True},
    {"object": "a tree", "animal": False, "vegetable": True,
     "living": True, "bigger": True, "outside": True},
    {"object": "a cat", "animal": True, "vegetable": False,
     "living": True, "domestic": True, "bigger": False},
    {"object": "Iron Man's suit", "animal": False, "vegetable": False,
     "metal": True, "fictional": True, "flies": True},
]

_twenty_q: dict = {}
_story_game: dict = {}
_word_assoc: dict = {}


# ── Word Association ───────────────────────────────────────────────────────────

def start_word_association(starter: str = "") -> str:
    global _word_assoc
    word = starter.lower() if starter else random.choice(list(_WORD_ASSOCIATIONS.keys()))
    _word_assoc = {"last_word": word, "chain": [word], "active": True}
    return f"Word association! I say: '{word}'. Your turn, sir."


def continue_association(word: str) -> str:
    global _word_assoc
    if not _word_assoc.get("active"):
        return "No active word association game. Say 'word association' to start, sir."
    word = word.lower().strip()
    _word_assoc["chain"].append(word)
    # JARVIS responds with a related word
    last      = word
    responses = _WORD_ASSOCIATIONS.get(last, []) or [
        f"{last}ful", f"anti-{last}", "quantum", "electric", "digital"
    ]
    response = random.choice(responses)
    _word_assoc["chain"].append(response)
    _word_assoc["last_word"] = response
    return f"'{response}'. Your turn, sir. Chain length: {len(_word_assoc['chain'])}."


# ── 20 Questions ───────────────────────────────────────────────────────────────

def start_twenty_questions() -> str:
    global _twenty_q
    obj = random.choice(_20Q_OBJECTS)
    _twenty_q = {"object": obj, "questions": 0, "active": True}
    return "Twenty questions! I'm thinking of something. Ask yes/no questions, sir."


def answer_question(question: str) -> str:
    global _twenty_q
    if not _twenty_q.get("active"):
        return "No active 20 questions game. Say 'twenty questions' to start, sir."
    _twenty_q["questions"] += 1
    obj = _twenty_q["object"]
    q   = question.lower()

    answer = "I don't know, sir."
    if "animal" in q:     answer = "Yes, sir." if obj.get("animal") else "No, sir."
    elif "vegetable" in q: answer = "Yes, sir." if obj.get("vegetable") else "No, sir."
    elif "metal" in q:    answer = "Yes, sir." if obj.get("metal") else "No, sir."
    elif "living" in q:   answer = "Yes, sir." if obj.get("living") else "No, sir."
    elif "flies" in q or "fly" in q: answer = "Yes, sir." if obj.get("flies") else "No, sir."
    elif "big" in q or "large" in q: answer = "Yes, sir." if obj.get("bigger") else "No, sir."
    elif "france" in q:   answer = "Yes, sir." if obj.get("France") else "No, sir."

    remaining = 20 - _twenty_q["questions"]
    if _twenty_q["questions"] >= 20:
        _twenty_q["active"] = False
        return f"{answer} Game over! The answer was: {obj['object']}, sir."
    return f"{answer} {remaining} questions remaining."


def guess_twenty_q(guess: str) -> str:
    if not _twenty_q.get("active"):
        return "No active game, sir."
    obj = _twenty_q["object"]["object"]
    _twenty_q["active"] = False
    if guess.lower().strip() in obj.lower():
        return f"Correct! It was {obj}! You got it in {_twenty_q['questions']} questions, sir."
    return f"Wrong, sir. It was '{obj}'. Better luck next time."
