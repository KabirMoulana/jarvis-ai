"""
jarvis/skills/color_palette.py
Color palette tool — JARVIS converts and analyses colors.
Hex to RGB, color names, complementary colors, palettes.
"""
import colorsys
import re

_COLOR_NAMES = {
    "red": "#FF0000", "green": "#008000", "blue": "#0000FF",
    "yellow": "#FFFF00", "orange": "#FFA500", "purple": "#800080",
    "pink": "#FFC0CB", "black": "#000000", "white": "#FFFFFF",
    "grey": "#808080", "gray": "#808080", "cyan": "#00FFFF",
    "magenta": "#FF00FF", "brown": "#A52A2A", "gold": "#FFD700",
    "silver": "#C0C0C0", "navy": "#000080", "teal": "#008080",
    "lime": "#00FF00", "coral": "#FF7F50", "indigo": "#4B0082",
    "violet": "#EE82EE", "turquoise": "#40E0D0", "crimson": "#DC143C",
}


def hex_to_rgb(hex_color: str) -> str:
    hex_c = hex_color.strip().lstrip("#")
    if len(hex_c) == 3:
        hex_c = "".join(c*2 for c in hex_c)
    try:
        r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        return f"#{hex_c.upper()} = RGB({r}, {g}, {b}), sir."
    except ValueError:
        return f"Invalid hex color: {hex_color}, sir."


def rgb_to_hex(r: int, g: int, b: int) -> str:
    hex_c = f"#{r:02X}{g:02X}{b:02X}"
    return f"RGB({r}, {g}, {b}) = {hex_c}, sir."


def get_complementary(hex_color: str) -> str:
    hex_c = hex_color.strip().lstrip("#")
    try:
        r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        comp    = f"#{255-r:02X}{255-g:02X}{255-b:02X}"
        return f"Complementary of {hex_color}: {comp}, sir."
    except Exception:
        return f"Invalid hex color, sir."


def color_name_to_hex(name: str) -> str:
    name = name.lower().strip()
    if name in _COLOR_NAMES:
        return f"{name.title()} = {_COLOR_NAMES[name]}, sir."
    return f"Color '{name}' not in database, sir."


def get_palette(base_hex: str, scheme: str = "complementary") -> str:
    """Generate a color palette from a base color."""
    hex_c = base_hex.strip().lstrip("#")
    try:
        r, g, b   = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        h, s, v   = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        colors    = []

        if scheme == "complementary":
            h2 = (h + 0.5) % 1
            r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
            colors = [base_hex, f"#{int(r2*255):02X}{int(g2*255):02X}{int(b2*255):02X}"]

        elif scheme == "triadic":
            for offset in [0, 1/3, 2/3]:
                h2 = (h + offset) % 1
                rr, gg, bb = colorsys.hsv_to_rgb(h2, s, v)
                colors.append(f"#{int(rr*255):02X}{int(gg*255):02X}{int(bb*255):02X}")

        elif scheme == "analogous":
            for offset in [-1/12, 0, 1/12]:
                h2 = (h + offset) % 1
                rr, gg, bb = colorsys.hsv_to_rgb(h2, s, v)
                colors.append(f"#{int(rr*255):02X}{int(gg*255):02X}{int(bb*255):02X}")

        return f"{scheme.title()} palette: " + ", ".join(colors) + ", sir."
    except Exception as e:
        return f"Palette generation failed: {e}"
