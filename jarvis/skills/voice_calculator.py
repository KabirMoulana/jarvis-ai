"""
jarvis/skills/voice_calculator.py
Voice calculator — parses natural language math expressions.
"What is 15 percent of 340" / "Square root of 144" / "2 to the power of 10"
"""
import math
import re


def calculate_natural(expression: str) -> str:
    """Parse and evaluate a natural language math expression."""
    expr = expression.lower().strip()

    # Percentage of
    m = re.search(r"(\d+\.?\d*)\s*percent\s+of\s+(\d+\.?\d*)", expr)
    if m:
        pct, total = float(m.group(1)), float(m.group(2))
        result = (pct / 100) * total
        return f"{pct}% of {total} is {result:,.2f}, sir."

    # Percentage change
    m = re.search(r"percentage\s+(?:change|increase|decrease)\s+from\s+(\d+\.?\d*)\s+to\s+(\d+\.?\d*)", expr)
    if m:
        old, new = float(m.group(1)), float(m.group(2))
        change   = ((new - old) / old) * 100
        direction = "increase" if change >= 0 else "decrease"
        return f"That's a {abs(change):.1f}% {direction}, sir."

    # Square root
    m = re.search(r"square\s+root\s+of\s+(\d+\.?\d*)", expr)
    if m:
        n = float(m.group(1))
        return f"Square root of {n} is {math.sqrt(n):.4f}, sir."

    # Power
    m = re.search(r"(\d+\.?\d*)\s+(?:to\s+the\s+power\s+of|raised\s+to|squared|cubed|\^)\s*(\d+\.?\d*)?", expr)
    if m:
        base = float(m.group(1))
        if "squared" in expr:   exp = 2
        elif "cubed" in expr:   exp = 3
        else:                    exp = float(m.group(2) or 2)
        return f"{base} to the power of {exp:.0f} is {base**exp:,.2f}, sir."

    # Factorial
    m = re.search(r"factorial\s+of\s+(\d+)", expr)
    if m:
        n = int(m.group(1))
        if n > 20:
            return "That factorial is astronomically large, sir."
        return f"Factorial of {n} is {math.factorial(n):,}, sir."

    # Average / mean
    nums = re.findall(r"\d+\.?\d*", expr)
    if "average" in expr or "mean" in expr:
        if nums:
            values = list(map(float, nums))
            avg    = sum(values) / len(values)
            return f"Average of {', '.join(nums)} is {avg:.2f}, sir."

    # Sum
    if "sum" in expr or "add" in expr or "total" in expr:
        if nums:
            values = list(map(float, nums))
            return f"Sum of {', '.join(nums)} is {sum(values):,.2f}, sir."

    # Generic expression
    try:
        cleaned = re.sub(r"[^\d\.\+\-\*\/\(\)\%\s]", "", expr).strip()
        if cleaned:
            result = eval(cleaned, {"__builtins__": {}}, {})
            return f"The answer is {result:,}, sir."
    except Exception:
        pass

    return f"I couldn't parse that mathematical expression, sir. Try rephrasing."
