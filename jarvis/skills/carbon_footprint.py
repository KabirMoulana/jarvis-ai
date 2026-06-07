"""
jarvis/skills/carbon_footprint.py
Carbon footprint calculator — JARVIS estimates your
environmental impact and suggests ways to reduce it.
"""

_EMISSION_FACTORS = {
    "flight_short":   0.255,   # kg CO2 per km (< 3h)
    "flight_long":    0.195,   # kg CO2 per km (> 3h)
    "car_petrol":     0.192,   # kg CO2 per km
    "car_diesel":     0.171,   # kg CO2 per km
    "car_electric":   0.053,   # kg CO2 per km (UK grid)
    "train":          0.041,   # kg CO2 per km
    "bus":            0.089,   # kg CO2 per km
    "beef_meal":      6.61,    # kg CO2 per meal
    "chicken_meal":   0.86,    # kg CO2 per meal
    "vegetarian_meal":0.33,    # kg CO2 per meal
    "vegan_meal":     0.21,    # kg CO2 per meal
    "electricity_kwh":0.233,   # kg CO2 per kWh (UK average)
    "streaming_hour": 0.036,   # kg CO2 per hour
}

_OFFSETS = {
    "tree_per_year":  21.0,    # kg CO2 absorbed per tree per year
    "solar_panel_kwh":0.0,     # effectively zero
}


def calculate_flight(distance_km: float, is_long_haul: bool = False) -> str:
    factor = _EMISSION_FACTORS["flight_long" if is_long_haul else "flight_short"]
    co2    = distance_km * factor
    trees  = co2 / _OFFSETS["tree_per_year"]
    return (
        f"Flight of {distance_km:,.0f}km emits approximately {co2:,.1f}kg CO2, sir. "
        f"Equivalent to {trees:.1f} trees absorbing carbon for a year."
    )


def calculate_commute(distance_km: float, vehicle: str = "car_petrol",
                      days_per_year: int = 230) -> str:
    factor  = _EMISSION_FACTORS.get(vehicle, _EMISSION_FACTORS["car_petrol"])
    daily   = distance_km * 2 * factor
    annual  = daily * days_per_year
    vs_train = distance_km * 2 * _EMISSION_FACTORS["train"] * days_per_year
    saving  = annual - vs_train
    return (
        f"Annual commute emissions ({vehicle}): {annual:,.1f}kg CO2, sir. "
        f"Switching to train would save {saving:,.1f}kg CO2/year."
    )


def calculate_diet_impact(meals_per_week: dict) -> str:
    """
    meals_per_week: {'beef': 3, 'chicken': 4, 'vegetarian': 7, 'vegan': 0}
    """
    weekly_co2 = 0
    for meal_type, count in meals_per_week.items():
        key = f"{meal_type}_meal"
        if key in _EMISSION_FACTORS:
            weekly_co2 += _EMISSION_FACTORS[key] * count
    annual_co2  = weekly_co2 * 52
    if all(meals_per_week.get(t, 0) == 0 for t in ["beef", "chicken"]):
        tip = "Your plant-based diet has a low carbon footprint, sir."
    elif meals_per_week.get("beef", 0) > 2:
        tip = "Reducing beef to once a week could cut food emissions by 30%, sir."
    else:
        tip = "Consider swapping one meat meal per week for a plant-based option, sir."
    return f"Annual diet emissions: {annual_co2:,.1f}kg CO2. {tip}"


def get_reduction_tips() -> str:
    tips = [
        "Switch to a renewable energy tariff — could cut home emissions by 50%.",
        "One less transatlantic flight per year saves 1.5 tonnes of CO2.",
        "A plant-based diet can reduce food emissions by up to 73%.",
        "Electric cars emit 3x less CO2 over their lifetime than petrol cars.",
        "Turn off devices at the plug — standby power costs 10% of home energy use.",
        "Buying second-hand extends product life and avoids manufacturing emissions.",
    ]
    import random
    return "Carbon reduction tip, sir: " + random.choice(tips)
