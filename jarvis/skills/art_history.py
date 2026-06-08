"""Art history — JARVIS explains art movements and famous works."""
import random

_MOVEMENTS = {
    "renaissance": "The Renaissance (14th-17th century) was a cultural rebirth rooted in classical antiquity. Key artists: Leonardo da Vinci, Michelangelo, Raphael, sir.",
    "impressionism": "Impressionism (1860s-1880s) captured fleeting moments with loose brushwork and natural light. Key artists: Monet, Renoir, Degas, sir.",
    "cubism": "Cubism (1907-1920s) fragmented objects into geometric shapes from multiple viewpoints simultaneously. Key artists: Picasso, Braque, sir.",
    "surrealism": "Surrealism (1920s-1950s) explored the unconscious mind and dreamlike imagery. Key artists: Dalí, Magritte, Ernst, sir.",
    "abstract expressionism": "Abstract Expressionism (1940s-50s) emphasised emotion over representation. Key artists: Pollock, de Kooning, Rothko, sir.",
    "baroque": "The Baroque period (17th century) used dramatic light, movement, and emotion. Key artists: Caravaggio, Rembrandt, Vermeer, sir.",
    "romanticism": "Romanticism (late 18th-19th century) celebrated emotion, nature, and individualism. Key artists: Turner, Delacroix, Friedrich, sir.",
    "pop art": "Pop Art (1950s-60s) embraced popular culture and mass media imagery. Key artists: Warhol, Lichtenstein, Hockney, sir.",
}

_FACTS = [
    "The Mona Lisa is painted on a poplar wood panel, not canvas, sir.",
    "Van Gogh only sold one painting during his lifetime — The Red Vineyard, sir.",
    "The Sistine Chapel ceiling took Michelangelo 4 years to paint (1508-1512), sir.",
    "Picasso could draw before he could walk, according to his mother, sir.",
    "The Louvre in Paris is the world's most visited art museum, sir.",
    "Leonardo da Vinci was also an engineer, scientist, musician, and inventor, sir.",
]

def get_movement(name: str) -> str:
    for key, desc in _MOVEMENTS.items():
        if key in name.lower() or name.lower() in key:
            return desc
    return f"Movement not found. Available: {', '.join(_MOVEMENTS.keys())}, sir."

def get_art_fact() -> str:
    return random.choice(_FACTS)

def list_movements() -> str:
    return f"Art movements: {', '.join(_MOVEMENTS.keys())}, sir."
