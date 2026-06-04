"""
jarvis/skills/trivia.py
Trivia game — JARVIS quizzes you with random trivia questions.
Uses the Open Trivia Database API (free, no key).
"""
import urllib.request
import urllib.parse
import json
import html
import random

_API = "https://opentdb.com/api.php"
_current_question: dict = {}

_CATEGORIES = {
    "general":    9,  "books":     10, "film":      11,
    "music":      12, "science":   17, "computers": 18,
    "maths":      19, "sports":    21, "geography": 22,
    "history":    23, "politics":  24, "art":       25,
    "celebrities":26, "animals":   27, "vehicles":  28,
}


def get_trivia(category: str = "", difficulty: str = "medium") -> str:
    """Fetch a trivia question and store it for answer checking."""
    global _current_question
    params = {"amount": 1, "type": "multiple", "difficulty": difficulty}

    cat_id = None
    if category:
        for key, val in _CATEGORIES.items():
            if category.lower() in key:
                cat_id = val
                break
    if cat_id:
        params["category"] = cat_id

    try:
        url = f"{_API}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        q = data["results"][0]

        question   = html.unescape(q["question"])
        correct    = html.unescape(q["correct_answer"])
        wrong      = [html.unescape(a) for a in q["incorrect_answers"]]
        options    = wrong + [correct]
        random.shuffle(options)

        _current_question = {
            "question":  question,
            "correct":   correct,
            "options":   options,
            "category":  q["category"],
            "difficulty": q["difficulty"],
        }

        opts_str = " | ".join(f"{chr(65+i)}. {opt}" for i, opt in enumerate(options))
        return (
            f"Trivia ({q['category']} — {q['difficulty']}): {question} "
            f"Options: {opts_str}"
        )
    except Exception as e:
        return f"Trivia fetch failed: {e}"


def check_trivia_answer(answer: str) -> str:
    """Check the answer to the current trivia question."""
    if not _current_question:
        return "No active trivia question, sir. Say 'trivia question' to start."

    correct = _current_question["correct"]
    options = _current_question["options"]
    answer  = answer.strip()

    # Accept letter (A/B/C/D) or full answer text
    if len(answer) == 1 and answer.upper() in "ABCD":
        idx      = ord(answer.upper()) - 65
        selected = options[idx] if idx < len(options) else ""
    else:
        selected = answer

    if selected.lower() == correct.lower():
        return f"Correct, sir! The answer is '{correct}'."
    return f"Wrong, sir. The correct answer is '{correct}'."


def list_categories() -> str:
    cats = ", ".join(_CATEGORIES.keys())
    return f"Trivia categories: {cats}, sir."
