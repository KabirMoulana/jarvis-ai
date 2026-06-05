"""
jarvis/skills/interview_prep.py
Interview prep — JARVIS quizzes you on technical and
behavioural interview questions.
"""
import random
import json
import os
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "interview_scores.json")

_QUESTIONS = {
    "behavioural": [
        "Tell me about a time you faced a major challenge at work.",
        "Describe a situation where you had to work with a difficult teammate.",
        "Give an example of a time you showed leadership.",
        "Tell me about your greatest professional achievement.",
        "Describe a time you failed and what you learned from it.",
        "How do you handle tight deadlines and pressure?",
        "Tell me about a time you had to adapt to a significant change.",
    ],
    "technical": [
        "Explain the difference between a list and a tuple in Python.",
        "What is Big O notation and why does it matter?",
        "Explain REST vs GraphQL.",
        "What is the difference between SQL and NoSQL databases?",
        "Explain how Git branching works.",
        "What is recursion? Give an example.",
        "Explain object-oriented programming principles.",
        "What is a race condition and how do you prevent it?",
        "Explain the difference between synchronous and asynchronous code.",
    ],
    "system design": [
        "How would you design a URL shortener like bit.ly?",
        "Design a chat application like WhatsApp.",
        "How would you build a recommendation system?",
        "Design a rate limiter for an API.",
        "How would you scale a database for millions of users?",
    ],
    "iron man": [
        "How would you design an AI assistant like JARVIS?",
        "Describe the architecture of a real-time voice processing system.",
        "How would you implement a distributed system for global coverage?",
        "Design a secure authentication system for a superhero suit.",
    ],
}

_active_question: dict = {}


def get_question(category: str = "") -> str:
    global _active_question
    category = category.lower().strip()
    pool     = None

    for key in _QUESTIONS:
        if category in key or key in category:
            pool = _QUESTIONS[key]
            break

    if pool is None:
        all_q = [q for questions in _QUESTIONS.values() for q in questions]
        pool  = all_q

    question = random.choice(pool)
    _active_question = {"question": question, "category": category or "general"}
    return f"Interview question: {question}"


def get_answer_tip() -> str:
    """Return tips for answering the current question."""
    if not _active_question:
        return "No active question, sir."
    q = _active_question["question"].lower()
    if "time you" in q or "describe a" in q or "tell me about" in q:
        return (
            "Use the STAR method, sir: "
            "Situation, Task, Action, Result. "
            "Keep it concise — 2 minutes max."
        )
    elif "design" in q:
        return (
            "Start with requirements, then high-level design, "
            "then dive into components. Consider scale, availability, "
            "and trade-offs, sir."
        )
    elif "explain" in q or "difference" in q:
        return (
            "Give a clear definition first, then a concrete example. "
            "Mention trade-offs if applicable, sir."
        )
    return "Take a moment to structure your answer before speaking, sir."


def list_categories() -> str:
    cats = ", ".join(_QUESTIONS.keys())
    return f"Interview question categories: {cats}, sir."


def get_random_tip() -> str:
    tips = [
        "Research the company before every interview, sir.",
        "Prepare 3 questions to ask the interviewer.",
        "Use the STAR method for behavioural questions.",
        "Always clarify the problem before jumping to a solution.",
        "Think out loud during technical interviews — process matters.",
        "Practice your answers out loud, not just in your head.",
        "Arrive 10 minutes early — or log in 5 minutes early for virtual.",
    ]
    return random.choice(tips) + " — JARVIS."
