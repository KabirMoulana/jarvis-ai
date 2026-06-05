"""
jarvis/skills/food_nutrition.py
Food and nutrition lookup — JARVIS looks up calories,
macros, and nutrition info using the Open Food Facts API.
"""
import urllib.request
import urllib.parse
import json


_API = "https://world.openfoodfacts.org/cgi/search.pl"


def get_nutrition(food: str) -> str:
    """Get nutrition information for a food item."""
    try:
        params = urllib.parse.urlencode({
            "search_terms":   food,
            "search_simple":  1,
            "action":         "process",
            "json":           1,
            "page_size":      1,
            "fields":         "product_name,nutriments,serving_size",
        })
        url = f"{_API}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())

        products = data.get("products", [])
        if not products:
            return _calorie_fallback(food)

        p         = products[0]
        name      = p.get("product_name", food)
        n         = p.get("nutriments", {})
        calories  = n.get("energy-kcal_100g", n.get("energy_100g", 0))
        protein   = n.get("proteins_100g", 0)
        carbs     = n.get("carbohydrates_100g", 0)
        fat       = n.get("fat_100g", 0)
        serving   = p.get("serving_size", "100g")

        return (
            f"{name} (per {serving}): "
            f"{calories:.0f} kcal, "
            f"protein {protein:.1f}g, "
            f"carbs {carbs:.1f}g, "
            f"fat {fat:.1f}g, sir."
        )
    except Exception as e:
        return _calorie_fallback(food)


def _calorie_fallback(food: str) -> str:
    """Approximate calories for common foods."""
    approx = {
        "apple": "~95 kcal",      "banana": "~105 kcal",  "egg": "~70 kcal",
        "rice":  "~200 kcal/cup", "bread":  "~80 kcal/slice", "milk": "~150 kcal/cup",
        "chicken breast": "~165 kcal/100g", "salmon": "~208 kcal/100g",
        "pasta": "~220 kcal/100g", "pizza":  "~266 kcal/slice",
        "coffee": "~5 kcal",      "coca cola": "~140 kcal/can",
    }
    for key, val in approx.items():
        if key in food.lower():
            return f"Approximate calories for {key}: {val}, sir."
    return f"Nutrition data for '{food}' not available, sir. Try a more specific product name."


def calculate_daily_calories(weight_kg: float, height_cm: float,
                              age: int, gender: str = "male",
                              activity: str = "moderate") -> str:
    """Calculate recommended daily calorie intake (Mifflin-St Jeor)."""
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multipliers = {
        "sedentary": 1.2, "light": 1.375, "moderate": 1.55,
        "active": 1.725, "very active": 1.9
    }
    mult = multipliers.get(activity.lower(), 1.55)
    tdee = bmr * mult

    return (
        f"Your estimated daily calorie needs, sir: "
        f"{tdee:.0f} kcal/day ({activity} activity level). "
        f"BMR: {bmr:.0f} kcal. "
        f"For weight loss: {tdee-500:.0f} kcal. "
        f"For muscle gain: {tdee+250:.0f} kcal."
    )


def get_water_recommendation(weight_kg: float) -> str:
    """Calculate recommended daily water intake."""
    ml = weight_kg * 35
    glasses = ml / 250
    return f"Recommended water intake for {weight_kg}kg: {ml:.0f}ml ({glasses:.0f} glasses) per day, sir."
