"""
jarvis/skills/recipe_finder.py
Recipe finder — JARVIS suggests recipes based on ingredients
you have. Uses TheMealDB free API.
"""
import urllib.request
import urllib.parse
import json
import random

_API = "https://www.themealdb.com/api/json/v1/1"


def find_by_ingredient(ingredient: str) -> str:
    """Find recipes containing a specific ingredient."""
    try:
        url = f"{_API}/filter.php?i={urllib.parse.quote(ingredient)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data  = json.loads(resp.read())
        meals = data.get("meals") or []
        if not meals:
            return f"No recipes found with {ingredient}, sir."
        picks = random.sample(meals, min(3, len(meals)))
        names = ", ".join(m["strMeal"] for m in picks)
        return f"With {ingredient} you could make: {names}, sir. Say 'recipe for [name]' for details."
    except Exception as e:
        return f"Recipe search failed: {e}"


def get_recipe(name: str) -> str:
    """Get full recipe details for a dish."""
    try:
        url = f"{_API}/search.php?s={urllib.parse.quote(name)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data  = json.loads(resp.read())
        meals = data.get("meals") or []
        if not meals:
            return f"Recipe for '{name}' not found, sir."
        meal     = meals[0]
        title    = meal["strMeal"]
        category = meal["strCategory"]
        area     = meal["strArea"]
        # Extract ingredients
        ingredients = []
        for i in range(1, 21):
            ing  = meal.get(f"strIngredient{i}", "").strip()
            meas = meal.get(f"strMeasure{i}", "").strip()
            if ing:
                ingredients.append(f"{meas} {ing}".strip())
        ing_list = ", ".join(ingredients[:8])
        instr    = meal.get("strInstructions", "")[:200]
        return (
            f"{title} — {area} {category}. "
            f"You'll need: {ing_list}. "
            f"Instructions: {instr}..."
        )
    except Exception as e:
        return f"Recipe lookup failed: {e}"


def random_recipe() -> str:
    """Get a random recipe suggestion."""
    try:
        url = f"{_API}/random.php"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        meal = data["meals"][0]
        return (
            f"How about {meal['strMeal']}, sir? "
            f"It's a {meal['strArea']} {meal['strCategory']}. "
            f"Say 'recipe for {meal['strMeal']}' for full instructions."
        )
    except Exception as e:
        return f"Random recipe failed: {e}"


def find_by_category(category: str) -> str:
    """List meals in a category."""
    try:
        url = f"{_API}/filter.php?c={urllib.parse.quote(category)}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data  = json.loads(resp.read())
        meals = data.get("meals") or []
        if not meals:
            return f"No meals found in category '{category}', sir."
        picks = random.sample(meals, min(4, len(meals)))
        names = ", ".join(m["strMeal"] for m in picks)
        return f"{category} options: {names}, sir."
    except Exception as e:
        return f"Category search failed: {e}"
