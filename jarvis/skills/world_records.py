"""World records — JARVIS knows fascinating world records."""
import random

_RECORDS = {
    "fastest human": "Usain Bolt holds the 100m world record at 9.58 seconds (2009), sir.",
    "tallest building": "The Burj Khalifa in Dubai stands at 828 metres — tallest in the world, sir.",
    "longest flight": "The longest non-stop commercial flight is Singapore to New York at ~18 hours, sir.",
    "deepest dive": "Victor Vescovo reached 10,928m in the Mariana Trench in 2019, sir.",
    "fastest car": "The ThrustSSC holds the land speed record at 1,228 km/h (763 mph), sir.",
    "heaviest animal": "The blue whale is the heaviest animal at up to 200 tonnes, sir.",
    "longest living animal": "The Greenland shark can live for over 400 years, sir.",
    "hottest temperature": "The hottest recorded temperature on Earth was 56.7°C in Death Valley, California (1913), sir.",
    "coldest temperature": "The coldest recorded temperature was -89.2°C at Vostok Station, Antarctica, sir.",
    "most spoken language": "Mandarin Chinese has the most native speakers — approximately 900 million, sir.",
    "largest continent": "Asia is the largest continent, covering 44.6 million km², sir.",
    "oldest person": "Jeanne Calment of France lived to 122 years and 164 days (1875-1997), sir.",
    "fastest computer": "Frontier at Oak Ridge National Lab reached 1.1 exaflops in 2022, sir.",
    "most stars": "The observable universe contains an estimated 2 trillion galaxies each with billions of stars, sir.",
    "longest word": "The longest word in English is pneumonoultramicroscopicsilicovolcanoconiosis — a lung disease, sir.",
}

def get_record(category: str) -> str:
    for key, fact in _RECORDS.items():
        if key in category.lower() or category.lower() in key:
            return fact
    return (f"No record found for '{category}'. "
            f"Try: {', '.join(list(_RECORDS.keys())[:5])}, sir.")

def random_record() -> str:
    return random.choice(list(_RECORDS.values()))

def list_categories() -> str:
    return f"World record categories: {', '.join(_RECORDS.keys())}, sir."
