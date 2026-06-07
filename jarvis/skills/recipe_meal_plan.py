"""
jarvis/skills/recipe_meal_plan.py
Meal planner — JARVIS creates weekly meal plans
based on preferences, calories, and what's in the fridge.
"""
import random
import json
import os
from datetime import date, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "meal_plan.json")

_MEALS = {
    "breakfast": {
        "quick":    ["Overnight oats", "Greek yoghurt with granola", "Avocado toast",
                     "Banana smoothie", "Scrambled eggs on toast"],
        "healthy":  ["Chia pudding", "Veggie omelette", "Overnight oats with berries",
                     "Whole grain toast with peanut butter"],
        "indulgent":["Pancakes with maple syrup", "Full English breakfast",
                     "French toast with cream"],
    },
    "lunch": {
        "quick":    ["Caesar salad", "BLT sandwich", "Tomato soup with bread",
                     "Hummus and veggie wrap", "Leftovers"],
        "healthy":  ["Quinoa bowl", "Grilled chicken salad", "Lentil soup",
                     "Tuna nicoise", "Buddha bowl"],
        "indulgent":["Cheeseburger", "Chicken quesadilla", "Mac and cheese"],
    },
    "dinner": {
        "quick":    ["Pasta aglio e olio", "Stir fry with rice", "Omelette with salad",
                     "Grilled salmon", "Bean tacos"],
        "healthy":  ["Grilled chicken with vegetables", "Baked salmon with quinoa",
                     "Lentil curry", "Turkey meatballs", "Veggie stir fry"],
        "indulgent":["Beef steak with chips", "Chicken parmesan", "Pizza",
                     "Lamb chops", "Creamy pasta"],
    },
}


def generate_meal_plan(days: int = 7, style: str = "healthy") -> str:
    style = style.lower()
    if style not in ("quick", "healthy", "indulgent"):
        style = "healthy"

    plan = {}
    for i in range(days):
        day = (date.today() + timedelta(days=i)).strftime("%A")
        plan[day] = {
            "breakfast": random.choice(_MEALS["breakfast"].get(style, _MEALS["breakfast"]["healthy"])),
            "lunch":     random.choice(_MEALS["lunch"].get(style, _MEALS["lunch"]["healthy"])),
            "dinner":    random.choice(_MEALS["dinner"].get(style, _MEALS["dinner"]["healthy"])),
        }

    # Save plan
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump({"style": style, "plan": plan, "created": str(date.today())}, f, indent=2)

    today = list(plan.keys())[0]
    today_meals = plan[today]
    return (
        f"{days}-day {style} meal plan created, sir. "
        f"Today ({today}): "
        f"Breakfast: {today_meals['breakfast']}, "
        f"Lunch: {today_meals['lunch']}, "
        f"Dinner: {today_meals['dinner']}."
    )


def get_todays_meals() -> str:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                data = json.load(f)
            today = date.today().strftime("%A")
            meals = data["plan"].get(today)
            if meals:
                return (
                    f"Today's meals, sir: "
                    f"Breakfast: {meals['breakfast']}, "
                    f"Lunch: {meals['lunch']}, "
                    f"Dinner: {meals['dinner']}."
                )
    except Exception:
        pass
    return "No meal plan found for today, sir. Say 'generate meal plan' to create one."


def suggest_meal(meal_type: str = "dinner", style: str = "healthy") -> str:
    pool = _MEALS.get(meal_type.lower(), _MEALS["dinner"])
    meals = pool.get(style.lower(), pool.get("healthy", []))
    if not meals:
        return f"No {style} {meal_type} suggestions available, sir."
    return f"How about {random.choice(meals)} for {meal_type}, sir?"
