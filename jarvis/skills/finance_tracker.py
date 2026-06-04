"""
jarvis/skills/finance_tracker.py
Personal finance tracker — log expenses, income,
view summaries and budgets. All local, no bank API needed.
"""
import json
import os
from datetime import date, datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "finance.json")

_CATEGORIES = [
    "food", "transport", "entertainment", "health",
    "shopping", "utilities", "rent", "savings", "salary", "other"
]


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"transactions": [], "budget": {}}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def log_expense(amount: float, category: str = "other", note: str = "") -> str:
    data = _load()
    cat  = _match_category(category)
    entry = {
        "type":     "expense",
        "amount":   round(amount, 2),
        "category": cat,
        "note":     note,
        "date":     str(date.today()),
    }
    data["transactions"].append(entry)
    _save(data)
    return f"Expense of ${amount:.2f} logged under {cat}, sir."


def log_income(amount: float, source: str = "salary") -> str:
    data = _load()
    entry = {
        "type":     "income",
        "amount":   round(amount, 2),
        "category": source,
        "note":     "",
        "date":     str(date.today()),
    }
    data["transactions"].append(entry)
    _save(data)
    return f"Income of ${amount:.2f} from {source} logged, sir."


def get_monthly_summary() -> str:
    data   = _load()
    month  = date.today().strftime("%Y-%m")
    txns   = [t for t in data["transactions"] if t["date"].startswith(month)]

    income   = sum(t["amount"] for t in txns if t["type"] == "income")
    expenses = sum(t["amount"] for t in txns if t["type"] == "expense")
    balance  = income - expenses

    by_cat: dict[str, float] = {}
    for t in txns:
        if t["type"] == "expense":
            by_cat[t["category"]] = by_cat.get(t["category"], 0) + t["amount"]

    top_cats = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)[:3]
    cats_str = ", ".join(f"{k}: ${v:.2f}" for k, v in top_cats)

    return (
        f"This month's summary, sir. "
        f"Income: ${income:.2f}. Expenses: ${expenses:.2f}. "
        f"Balance: ${balance:+.2f}. "
        + (f"Top spending: {cats_str}." if cats_str else "No expenses logged yet.")
    )


def set_budget(category: str, amount: float) -> str:
    data = _load()
    cat  = _match_category(category)
    data["budget"][cat] = amount
    _save(data)
    return f"Monthly budget for {cat} set to ${amount:.2f}, sir."


def check_budget(category: str) -> str:
    data   = _load()
    cat    = _match_category(category)
    budget = data["budget"].get(cat, 0)
    if not budget:
        return f"No budget set for {cat}, sir."
    month  = date.today().strftime("%Y-%m")
    spent  = sum(
        t["amount"] for t in data["transactions"]
        if t["type"] == "expense" and t["category"] == cat and t["date"].startswith(month)
    )
    remaining = budget - spent
    pct       = spent / budget * 100
    status    = "over budget" if remaining < 0 else f"${remaining:.2f} remaining"
    return f"{cat.capitalize()} budget: ${budget:.2f}. Spent: ${spent:.2f} ({pct:.0f}%). {status}, sir."


def _match_category(name: str) -> str:
    name = name.lower().strip()
    for cat in _CATEGORIES:
        if name in cat or cat in name:
            return cat
    return "other"
