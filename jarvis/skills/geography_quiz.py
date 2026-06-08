"""Geography quiz — JARVIS quizzes you on world geography."""
import random, json, os
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "geo_scores.json")

_QUESTIONS = [
    ("What is the capital of Australia?", "Canberra"),
    ("What is the largest country by area?", "Russia"),
    ("What is the longest river in the world?", "Nile"),
    ("What is the smallest country in the world?", "Vatican City"),
    ("What is the highest mountain in the world?", "Mount Everest"),
    ("What country has the most natural lakes?", "Canada"),
    ("What is the capital of Brazil?", "Brasília"),
    ("What ocean is the largest?", "Pacific"),
    ("What country is the Amazon rainforest mostly in?", "Brazil"),
    ("What is the capital of Canada?", "Ottawa"),
    ("What is the deepest lake in the world?", "Lake Baikal"),
    ("What continent is Egypt in?", "Africa"),
    ("What is the capital of Japan?", "Tokyo"),
    ("What is the largest desert in the world?", "Sahara"),
    ("What country has the most spoken languages?", "Papua New Guinea"),
]

_active: dict = {}

def get_question() -> str:
    global _active
    q, a = random.choice(_QUESTIONS)
    _active = {"question": q, "answer": a.lower()}
    return f"Geography question, sir: {q}"

def check_answer(answer: str) -> str:
    if not _active:
        return "No active question. Say 'geography quiz', sir."
    correct = _active["answer"]
    if answer.lower().strip() in correct or correct in answer.lower().strip():
        _update_score(True)
        return f"Correct! The answer is {_active['answer'].title()}, sir."
    _update_score(False)
    return f"Wrong. The answer is {_active['answer'].title()}, sir."

def _update_score(correct: bool):
    try:
        data = {}
        if os.path.exists(_FILE):
            with open(_FILE) as f: data = json.load(f)
        today = str(date.today())
        if today not in data: data[today] = {"correct": 0, "total": 0}
        data[today]["total"] += 1
        if correct: data[today]["correct"] += 1
        os.makedirs(os.path.dirname(_FILE), exist_ok=True)
        with open(_FILE, "w") as f: json.dump(data, f)
    except Exception: pass

def get_score() -> str:
    try:
        if not os.path.exists(_FILE): return "No scores yet, sir."
        with open(_FILE) as f: data = json.load(f)
        total = sum(d["total"] for d in data.values())
        correct = sum(d["correct"] for d in data.values())
        pct = int(correct/total*100) if total else 0
        return f"Geography score: {correct}/{total} ({pct}%), sir."
    except Exception: return "Score data unavailable, sir."
