"""Cooking timer — JARVIS times specific cooking tasks with expert guidance."""
import threading, time

_COOKING_TIMES = {
    "pasta": (480, "Cook until al dente. Salt the water generously first, sir."),
    "rice": (1080, "Cover and simmer on low heat. Don't lift the lid, sir."),
    "boiled egg soft": (360, "Soft boiled — runny yolk. Plunge in cold water immediately, sir."),
    "boiled egg hard": (600, "Hard boiled — fully set yolk, sir."),
    "chicken breast": (1320, "Cook to 75°C internal temperature. Rest for 5 minutes, sir."),
    "steak medium": (480, "Medium steak — pink centre. Rest for equal time after cooking, sir."),
    "salmon": (480, "Salmon is done when it flakes easily with a fork, sir."),
    "vegetables": (300, "Blanch until just tender — don't overcook, sir."),
    "bread": (1800, "Bake until hollow when tapped on the bottom, sir."),
    "cake": (2100, "Test with a skewer — it should come out clean, sir."),
    "cookies": (720, "Take out while still slightly soft — they firm up as they cool, sir."),
    "french fries": (900, "Fry in batches at 180°C for crispy results, sir."),
    "bacon": (480, "Cook to your preferred crispness. Low and slow for flat bacon, sir."),
    "pizza": (900, "Preheat your oven as hot as it goes for best results, sir."),
}

_active_timers: dict = {}

def start_cooking_timer(food: str, callback=None) -> str:
    food_lower = food.lower().strip()
    match = None
    for key, (secs, tip) in _COOKING_TIMES.items():
        if key in food_lower or food_lower in key:
            match = (key, secs, tip)
            break
    if not match:
        foods = ", ".join(_COOKING_TIMES.keys())
        return f"No timer preset for '{food}', sir. Available: {foods}."
    name, secs, tip = match
    mins = secs // 60

    def _fire():
        msg = f"{name.title()} is ready, sir! {tip}"
        print(f"\n🍳  {msg}")
        if callback: callback(msg)

    t = threading.Timer(secs, _fire)
    t.daemon = True
    t.start()
    _active_timers[name] = t
    return f"{name.title()} timer set for {mins} minutes. {tip}"

def get_cooking_tip(food: str) -> str:
    for key, (_, tip) in _COOKING_TIMES.items():
        if key in food.lower() or food.lower() in key:
            return f"Cooking tip for {key}: {tip}"
    return f"No specific tip for '{food}', sir."

def list_presets() -> str:
    items = [f"{k} ({v[0]//60}min)" for k, v in list(_COOKING_TIMES.items())[:8]]
    return "Cooking presets: " + ", ".join(items) + ", sir."
