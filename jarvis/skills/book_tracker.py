"""
jarvis/skills/book_tracker.py
Book tracker — JARVIS manages your reading list.
Track books you're reading, have read, and want to read.
Uses Open Library API for book info.
"""
import json
import os
import urllib.request
import urllib.parse
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "books.json")
_STATUSES = ("reading", "read", "want to read")


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(data: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def add_book(title: str, author: str = "", status: str = "want to read") -> str:
    data   = _load()
    status = status.lower().strip()
    if status not in _STATUSES:
        status = "want to read"
    entry = {
        "title":   title.strip(),
        "author":  author.strip(),
        "status":  status,
        "added":   str(date.today()),
        "rating":  0,
        "notes":   "",
    }
    data.append(entry)
    _save(data)
    return f"'{title}' added to your {status} list, sir."


def update_status(title: str, status: str) -> str:
    data = _load()
    for b in data:
        if title.lower() in b["title"].lower():
            b["status"] = status.lower()
            if status.lower() == "read":
                b["finished"] = str(date.today())
            _save(data)
            return f"'{b['title']}' marked as {status}, sir."
    return f"Book '{title}' not found, sir."


def rate_book(title: str, rating: int) -> str:
    data   = _load()
    rating = max(1, min(5, rating))
    for b in data:
        if title.lower() in b["title"].lower():
            b["rating"] = rating
            _save(data)
            stars = "★" * rating + "☆" * (5 - rating)
            return f"Rated '{b['title']}' {stars} ({rating}/5), sir."
    return f"Book '{title}' not found, sir."


def get_reading_list(status: str = "") -> str:
    data = _load()
    if status:
        books = [b for b in data if status.lower() in b["status"]]
    else:
        books = data
    if not books:
        return f"No books in your {status or 'full'} list, sir."
    by_status: dict[str, list] = {}
    for b in books:
        by_status.setdefault(b["status"], []).append(b["title"])
    parts = []
    for s, titles in by_status.items():
        parts.append(f"{s.title()}: {', '.join(titles[:3])}")
    return " | ".join(parts) + f". Total: {len(books)} book(s), sir."


def search_book_info(title: str) -> str:
    """Look up book info from Open Library."""
    try:
        encoded = urllib.parse.quote(title)
        url     = f"https://openlibrary.org/search.json?q={encoded}&limit=1&fields=title,author_name,first_publish_year,number_of_pages_median"
        req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        docs = data.get("docs", [])
        if not docs:
            return f"No info found for '{title}', sir."
        d      = docs[0]
        author = ", ".join(d.get("author_name", ["Unknown"])[:2])
        year   = d.get("first_publish_year", "Unknown")
        pages  = d.get("number_of_pages_median", "Unknown")
        return f"'{d['title']}' by {author}, first published {year}, approximately {pages} pages, sir."
    except Exception as e:
        return f"Book lookup failed: {e}"
