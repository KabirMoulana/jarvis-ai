"""
jarvis/skills/math_quiz.py
Math quiz — JARVIS tests your mental arithmetic.
Adjustable difficulty, tracks score, timed challenges.
"""
import random
import time

_active_question: dict = {}
_score = {"correct": 0, "total": 0, "streak": 0}


def get_math_question(difficulty: str = "medium") -> str:
    global _active_question
    difficulty = difficulty.lower()

    if difficulty == "easy":
        a, b = random.randint(1, 20), random.randint(1, 20)
        op   = random.choice(["+", "-"])
    elif difficulty == "hard":
        a, b = random.randint(10, 99), random.randint(10, 99)
        op   = random.choice(["+", "-", "*"])
    else:
        a, b = random.randint(1, 50), random.randint(1, 50)
        op   = random.choice(["+", "-", "*"])

    if op == "+": answer = a + b
    elif op == "-":
        if a < b: a, b = b, a
        answer = a - b
    else:
        a, b   = random.randint(2, 12), random.randint(2, 12)
        answer = a * b

    _active_question = {
        "question": f"{a} {op} {b}",
        "answer":   answer,
        "asked_at": time.time(),
    }
    return f"Math question: What is {a} {op} {b}?"


def check_math_answer(user_answer: str) -> str:
    global _score
    if not _active_question:
        return "No active question, sir. Say 'math question' to start."
    try:
        given = int(user_answer.strip())
    except ValueError:
        return "Please answer with a number, sir."

    correct  = _active_question["answer"]
    elapsed  = time.time() - _active_question.get("asked_at", time.time())
    _score["total"] += 1

    if given == correct:
        _score["correct"] += 1
        _score["streak"]  += 1
        speed  = f" ({elapsed:.1f}s)" if elapsed < 60 else ""
        streak = f" {_score['streak']} in a row!" if _score["streak"] > 1 else ""
        return f"Correct{speed}!{streak} The answer is {correct}, sir."
    else:
        _score["streak"] = 0
        return f"Wrong, sir. {_active_question['question']} = {correct}, not {given}."


def get_math_score() -> str:
    total   = _score["total"]
    correct = _score["correct"]
    if total == 0:
        return "No questions answered yet, sir."
    pct = int(correct / total * 100)
    return f"Math score: {correct}/{total} ({pct}%). Best streak: {_score['streak']}, sir."


def reset_score() -> str:
    global _score
    _score = {"correct": 0, "total": 0, "streak": 0}
    return "Math quiz score reset, sir."


def times_table(number: int) -> str:
    """Recite a times table."""
    lines = [f"{number} × {i} = {number * i}" for i in range(1, 13)]
    return f"Times table for {number}: " + ", ".join(lines) + ", sir."
