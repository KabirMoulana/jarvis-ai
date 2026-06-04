"""
jarvis/skills/shopping_list.py
Shopping list manager — JARVIS maintains your shopping list,
organises by category, and can open delivery apps.
"""
import json
import os
import webbrowser
import urllib.parse

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "shopping.json")

_CATEGORIES = {
    "produce":    ["apple", "banana", "tomato", "lettuce", "onion", "potato", "carrot", "spinach"],
    "dairy":      ["milk", "cheese", "butter", "yogurt", "cream", "eggs"],
    "meat":       ["chicken", "beef", "fish", "salmon", "pork", "lamb", "turkey"],
    "bakery":     ["bread", "rolls", "cake", "muffin", "baguette"],
    "drinks":     ["water", "juice", "coffee", "tea", "soda", "wine", "beer"],
    "snacks":     ["chips", "biscuits", "chocolate", "nuts", "popcorn", "crackers"],
    "household":  ["soap", "shampoo", "toothpaste", "detergent", "toilet paper", "tissues"],
    "frozen":     ["pizza", "ice cream", "frozen peas", "frozen chips"],
}


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
        json.dump(data, f, indent=2)


def _guess_category(item: str) -> str:
    item_lower = item.lower()
    for cat, items in _CATEGORIES.items():
        if any(i in item_lower for i in items):
            return cat
    return "other"


def add_item(item: str, quantity: str = "1", category: str = "") -> str:
    data = _load()
    cat  = category or _guess_category(item)
    data.append({
        "item":     item.strip(),
        "quantity": quantity,
        "category": cat,
        "checked":  False,
    })
    _save(data)
    return f"Added {quantity}x {item} to your shopping list, sir."


def remove_item(item: str) -> str:
    data   = _load()
    before = len(data)
    data   = [d for d in data if item.lower() not in d["item"].lower()]
    if len(data) < before:
        _save(data)
        return f"Removed {item} from shopping list, sir."
    return f"'{item}' not found in shopping list, sir."


def check_item(item: str) -> str:
    data = _load()
    for d in data:
        if item.lower() in d["item"].lower():
            d["checked"] = True
            _save(data)
            return f"'{d['item']}' checked off, sir."
    return f"'{item}' not found, sir."


def get_list(show_checked: bool = False) -> str:
    data  = _load()
    items = [d for d in data if show_checked or not d["checked"]]
    if not items:
        return "Shopping list is empty, sir."
    by_cat: dict[str, list] = {}
    for d in items:
        by_cat.setdefault(d["category"], []).append(f"{d['quantity']}x {d['item']}")
    parts = []
    for cat, items_list in by_cat.items():
        parts.append(f"{cat.title()}: {', '.join(items_list)}")
    total = len(items)
    return f"{total} item(s) on your list, sir. " + " | ".join(parts) + "."


def clear_checked() -> str:
    data = _load()
    data = [d for d in data if not d["checked"]]
    _save(data)
    return "Checked items cleared, sir."


def open_delivery_app(app: str = "uber eats") -> str:
    apps = {
        "uber eats":  "https://www.ubereats.com",
        "deliveroo":  "https://deliveroo.com",
        "just eat":   "https://www.just-eat.com",
        "doordash":   "https://www.doordash.com",
        "amazon":     "https://www.amazon.com/fresh",
    }
    url = apps.get(app.lower(), "https://www.ubereats.com")
    webbrowser.open(url)
    return f"Opening {app.title()}, sir."
