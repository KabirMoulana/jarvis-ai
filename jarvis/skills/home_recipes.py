"""Home recipes — JARVIS gives quick recipes from common ingredients."""
import random

_RECIPES = {
    "scrambled eggs": {
        "ingredients": ["eggs", "butter", "salt", "pepper", "milk"],
        "time": "5 minutes",
        "steps": ["Whisk eggs with a splash of milk.", "Melt butter in pan on low heat.",
                  "Add eggs and stir slowly with a spatula.", "Remove from heat while still slightly runny — residual heat finishes them."],
    },
    "pasta aglio e olio": {
        "ingredients": ["pasta", "garlic", "olive oil", "parsley", "chilli flakes"],
        "time": "15 minutes",
        "steps": ["Cook pasta until al dente.", "Slice garlic thinly and fry in olive oil until golden.",
                  "Add chilli flakes.", "Toss pasta in the oil, add parsley and pasta water."],
    },
    "banana smoothie": {
        "ingredients": ["banana", "milk", "honey", "ice"],
        "time": "3 minutes",
        "steps": ["Peel and slice banana.", "Add all ingredients to blender.",
                  "Blend until smooth.", "Serve immediately."],
    },
    "avocado toast": {
        "ingredients": ["bread", "avocado", "lemon", "salt", "pepper", "chilli flakes"],
        "time": "5 minutes",
        "steps": ["Toast bread.", "Mash avocado with lemon juice, salt and pepper.",
                  "Spread on toast.", "Top with chilli flakes."],
    },
    "fried rice": {
        "ingredients": ["rice", "egg", "soy sauce", "garlic", "spring onion", "oil"],
        "time": "10 minutes",
        "steps": ["Use day-old cold rice for best results.", "Fry garlic in hot oil.",
                  "Add rice and stir-fry.", "Push rice aside, scramble egg, then mix.",
                  "Add soy sauce and spring onion."],
    },
    "french omelette": {
        "ingredients": ["eggs", "butter", "salt", "herbs"],
        "time": "5 minutes",
        "steps": ["Beat eggs with salt.", "Melt butter in pan on medium heat.",
                  "Add eggs. Stir gently then let set.", "Roll omelette and serve immediately."],
    },
}

def get_recipe(name: str) -> str:
    for key, recipe in _RECIPES.items():
        if key in name.lower() or name.lower() in key:
            steps = " ".join(f"{i+1}. {s}" for i, s in enumerate(recipe["steps"]))
            return (f"{key.title()} ({recipe['time']}), sir. "
                    f"You need: {', '.join(recipe['ingredients'])}. "
                    f"Steps: {steps}")
    recipes = ", ".join(_RECIPES.keys())
    return f"Recipe for '{name}' not found. Available: {recipes}, sir."

def what_can_i_make(ingredients: list[str]) -> str:
    ingredients_lower = [i.lower() for i in ingredients]
    matches = []
    for name, recipe in _RECIPES.items():
        needed = recipe["ingredients"]
        have   = sum(1 for i in needed if any(i in x or x in i for x in ingredients_lower))
        if have >= len(needed) - 1:
            matches.append(f"{name.title()} (missing {len(needed)-have} ingredient(s))")
    if not matches:
        return "Nothing in my database matches those ingredients exactly, sir."
    return "You could make: " + " | ".join(matches) + ", sir."

def random_recipe() -> str:
    name, recipe = random.choice(list(_RECIPES.items()))
    return (f"How about {name.title()}? Ready in {recipe['time']}, "
            f"needs: {', '.join(recipe['ingredients'])}, sir.")
