"""Coding challenges — JARVIS gives you daily coding problems."""
import random
from datetime import date

_CHALLENGES = [
    {"title": "FizzBuzz", "difficulty": "easy",
     "problem": "Print numbers 1-100. For multiples of 3 print 'Fizz', multiples of 5 print 'Buzz', both print 'FizzBuzz'.",
     "hint": "Use the modulo operator (%), sir."},
    {"title": "Palindrome Check", "difficulty": "easy",
     "problem": "Write a function that checks if a string is a palindrome (reads the same forwards and backwards).",
     "hint": "Compare the string with its reverse: s == s[::-1], sir."},
    {"title": "Fibonacci", "difficulty": "easy",
     "problem": "Generate the first N numbers of the Fibonacci sequence.",
     "hint": "Each number is the sum of the two preceding ones, sir."},
    {"title": "Two Sum", "difficulty": "medium",
     "problem": "Given an array of integers and a target, return indices of two numbers that add up to the target.",
     "hint": "Use a hash map to store complements, sir."},
    {"title": "Valid Brackets", "difficulty": "medium",
     "problem": "Determine if a string of brackets (), [], {} is valid (properly opened and closed).",
     "hint": "Use a stack — push opening brackets, pop and match closing ones, sir."},
    {"title": "Binary Search", "difficulty": "medium",
     "problem": "Implement binary search on a sorted array.",
     "hint": "Divide the search space in half each iteration, sir."},
    {"title": "Merge Sort", "difficulty": "hard",
     "problem": "Implement the merge sort algorithm for an array of integers.",
     "hint": "Divide array in half, sort each half, then merge the sorted halves, sir."},
    {"title": "LRU Cache", "difficulty": "hard",
     "problem": "Design a Least Recently Used cache with O(1) get and put operations.",
     "hint": "Use a combination of a doubly linked list and a hash map, sir."},
    {"title": "Word Frequency", "difficulty": "easy",
     "problem": "Count the frequency of each word in a string and return the most common.",
     "hint": "Use Python's collections.Counter, sir."},
    {"title": "Anagram Check", "difficulty": "easy",
     "problem": "Check if two strings are anagrams of each other.",
     "hint": "Sort both strings and compare, or use Counter, sir."},
]

def get_daily_challenge() -> str:
    idx   = date.today().toordinal() % len(_CHALLENGES)
    c     = _CHALLENGES[idx]
    return (f"Daily coding challenge — {c['title']} ({c['difficulty']}), sir: "
            f"{c['problem']}")

def get_challenge_hint() -> str:
    idx = date.today().toordinal() % len(_CHALLENGES)
    c   = _CHALLENGES[idx]
    return f"Hint for {c['title']}: {c['hint']}"

def get_random_challenge(difficulty: str = "") -> str:
    pool = [c for c in _CHALLENGES if difficulty.lower() in c["difficulty"]] if difficulty else _CHALLENGES
    if not pool: pool = _CHALLENGES
    c = random.choice(pool)
    return (f"Coding challenge — {c['title']} ({c['difficulty']}), sir: {c['problem']}")

def list_difficulties() -> str:
    return "Challenge difficulties: easy, medium, hard, sir."
