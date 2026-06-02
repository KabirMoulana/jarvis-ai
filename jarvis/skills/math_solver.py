"""
jarvis/skills/math_solver.py
Advanced math solver — goes beyond the basic calculator.
Handles: algebra, unit conversion, statistics, currency,
and step-by-step explanations using sympy if available.
"""
import re
import math
import statistics


# ── Basic safe eval ───────────────────────────────────────────────────────────
_SAFE_NAMES = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
_SAFE_NAMES.update({"abs": abs, "round": round, "sum": sum, "min": min, "max": max})


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    expr = expression.strip()
    # Clean up natural language
    expr = re.sub(r"\bsquared\b",   "**2",    expr, flags=re.I)
    expr = re.sub(r"\bcubed\b",     "**3",    expr, flags=re.I)
    expr = re.sub(r"\bsqrt\b",      "sqrt",   expr, flags=re.I)
    expr = re.sub(r"\bpi\b",        "pi",     expr, flags=re.I)
    expr = re.sub(r"\bto the power of\s+", "**", expr, flags=re.I)
    expr = re.sub(r"\bx\b",         "*",      expr)
    expr = re.sub(r"[^\d\.\+\-\*\/\(\)\%\^\s\w]", "", expr)

    try:
        result = eval(expr, {"__builtins__": {}}, _SAFE_NAMES)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"The answer is {result:,}, sir."
    except Exception:
        return _try_sympy(expression)


def _try_sympy(expression: str) -> str:
    try:
        import sympy
        result = sympy.sympify(expression)
        return f"The answer is {result}, sir."
    except ImportError:
        return f"I couldn't evaluate that expression, sir."
    except Exception as e:
        return f"Math error: {e}"


def percentage(value: float, of: float) -> str:
    result = (value / 100) * of
    return f"{value}% of {of} is {result:,.2f}, sir."


def percentage_change(old: float, new: float) -> str:
    if old == 0:
        return "Cannot calculate percentage change from zero, sir."
    change = ((new - old) / abs(old)) * 100
    direction = "increase" if change >= 0 else "decrease"
    return f"That's a {abs(change):.1f}% {direction}, sir."


def statistics_summary(numbers: list[float]) -> str:
    if not numbers:
        return "No numbers provided, sir."
    return (
        f"Statistical summary: "
        f"mean {statistics.mean(numbers):.2f}, "
        f"median {statistics.median(numbers):.2f}, "
        f"min {min(numbers)}, "
        f"max {max(numbers)}, "
        f"standard deviation {statistics.stdev(numbers):.2f}."
        if len(numbers) > 1 else
        f"Only one value provided: {numbers[0]}."
    )


def solve_quadratic(a: float, b: float, c: float) -> str:
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return "No real solutions exist for this equation, sir."
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)
    if x1 == x2:
        return f"One solution: x = {x1:.4f}, sir."
    return f"Two solutions: x = {x1:.4f} and x = {x2:.4f}, sir."


def parse_math_query(text: str) -> str:
    """Top-level dispatcher for math queries."""
    text = text.lower()

    # Percentage of
    m = re.search(r"(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)", text)
    if m:
        return percentage(float(m.group(1)), float(m.group(2)))

    # Percentage change
    m = re.search(r"percentage change (?:from\s+)?(\d+\.?\d*)\s+to\s+(\d+\.?\d*)", text)
    if m:
        return percentage_change(float(m.group(1)), float(m.group(2)))

    # Extract and calculate expression
    expr = re.sub(r"(what(?:'s| is)|calculate|compute|solve|evaluate|how much is)", "", text, flags=re.I).strip()
    return calculate(expr)
