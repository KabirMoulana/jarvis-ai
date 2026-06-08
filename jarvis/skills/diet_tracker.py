"""Diet tracker — JARVIS logs meals and tracks macros."""
import json, os
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "diet.json")

_MACROS = {
    "apple": {"cal": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
    "banana": {"cal": 105, "protein": 1.3, "carbs": 27, "fat": 0.4},
    "egg": {"cal": 70, "protein": 6, "carbs": 0.6, "fat": 5},
    "rice": {"cal": 200, "protein": 4, "carbs": 44, "fat": 0.4},
    "chicken breast": {"cal": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "salmon": {"cal": 208, "protein": 20, "carbs": 0, "fat": 13},
    "bread": {"cal": 80, "protein": 3, "carbs": 15, "fat": 1},
    "milk": {"cal": 150, "protein": 8, "carbs": 12, "fat": 8},
    "pasta": {"cal": 220, "protein": 8, "carbs": 43, "fat": 1.3},
    "oats": {"cal": 150, "protein": 5, "carbs": 27, "fat": 3},
}

def _load():
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f: return json.load(f)
    except: pass
    return {}

def _save(data):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f: json.dump(data, f, indent=2)

def log_meal(food: str, servings: float = 1) -> str:
    data  = _load()
    today = str(date.today())
    food_lower = food.lower().strip()
    macros = None
    for key, vals in _MACROS.items():
        if key in food_lower or food_lower in key:
            macros = {k: round(v * servings, 1) for k, v in vals.items()}
            break
    if not macros:
        macros = {"cal": 0, "protein": 0, "carbs": 0, "fat": 0}
    if today not in data: data[today] = []
    data[today].append({"food": food, "servings": servings, **macros})
    _save(data)
    if macros["cal"]:
        return f"Logged {servings}x {food}: {macros['cal']} kcal, {macros['protein']}g protein, sir."
    return f"Logged {food} (no macro data). Add to database for tracking, sir."

def get_daily_totals() -> str:
    data  = _load()
    today = str(date.today())
    meals = data.get(today, [])
    if not meals: return "No meals logged today, sir."
    totals = {"cal": 0, "protein": 0, "carbs": 0, "fat": 0}
    for m in meals:
        for k in totals: totals[k] += m.get(k, 0)
    return (f"Today's nutrition, sir: {totals['cal']:.0f} kcal, "
            f"{totals['protein']:.1f}g protein, {totals['carbs']:.1f}g carbs, {totals['fat']:.1f}g fat.")

def get_meal_info(food: str) -> str:
    for key, vals in _MACROS.items():
        if key in food.lower() or food.lower() in key:
            return (f"{key.title()}: {vals['cal']} kcal, {vals['protein']}g protein, "
                    f"{vals['carbs']}g carbs, {vals['fat']}g fat per serving, sir.")
    return f"No macro data for '{food}', sir."
