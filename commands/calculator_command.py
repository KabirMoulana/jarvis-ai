
"""Evaluate simple math expressions from voice commands."""
import re


_SAFE_PATTERN = re.compile(r"^[\d\s\.\+\-\*\/\(\)\^\%]+$")


def evaluate(expr: str) -> str:
    expr = expr.replace("^", "**").replace("x", "*")
    if not _SAFE_PATTERN.match(expr):
        return "I can only evaluate simple math expressions."
    try:
        result = eval(expr, {"__builtins__": {}})
        return f"{expr} = {result}"
    except Exception:
        return f"Could not evaluate: {expr}"


def handle(command: str) -> str | None:
    triggers = ["calculate", "what is", "compute", "math"]
    for t in triggers:
        if t in command:
            expr = command
            for word in [t, "calculate", "what is", "compute", "math", "?"]:
                expr = expr.replace(word, "")
            expr = expr.strip()
            if re.search(r"[\d\+\-\*\/]", expr):
                return evaluate(expr)
    return None
