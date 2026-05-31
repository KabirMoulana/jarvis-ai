"""
jarvis/skills/calculator.py
Safe math expression evaluator and unit converter.
No eval() — uses the ast module to prevent code injection.
"""
import ast
import math
import operator
import re

# ── safe expression evaluator ─────────────────────────────────────────────────

_ALLOWED_OPS = {
    ast.Add:  operator.add,
    ast.Sub:  operator.sub,
    ast.Mult: operator.mul,
    ast.Div:  operator.truediv,
    ast.Pow:  operator.pow,
    ast.Mod:  operator.mod,
    ast.USub: operator.neg,
}

_ALLOWED_FUNCS = {
    "sqrt": math.sqrt,
    "sin":  math.sin,
    "cos":  math.cos,
    "tan":  math.tan,
    "log":  math.log,
    "log10":math.log10,
    "abs":  abs,
    "ceil": math.ceil,
    "floor":math.floor,
    "pi":   math.pi,
    "e":    math.e,
}

class _SafeEval(ast.NodeVisitor):
    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        op = _ALLOWED_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator not allowed: {node.op}")
        return op(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        op = _ALLOWED_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator not allowed: {node.op}")
        return op(self.visit(node.operand))

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed.")
        fn = _ALLOWED_FUNCS.get(node.func.id)
        if fn is None:
            raise ValueError(f"Function not allowed: {node.func.id}")
        args = [self.visit(a) for a in node.args]
        return fn(*args)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed.")

    def visit_Name(self, node):
        if node.id in _ALLOWED_FUNCS:
            return _ALLOWED_FUNCS[node.id]
        raise ValueError(f"Name not allowed: {node.id}")

    def generic_visit(self, node):
        raise ValueError(f"Node type not allowed: {type(node).__name__}")


def calculate(expression: str) -> str:
    """Evaluate a math expression safely and return the result as a string."""
    # replace common spoken words
    expr = expression.lower()
    expr = expr.replace("x", "*").replace("times", "*")
    expr = expr.replace("divided by", "/").replace("plus", "+").replace("minus", "-")
    expr = expr.replace("to the power of", "**").replace("squared", "**2")
    expr = re.sub(r"[^0-9+\-*/().%^ a-z]", "", expr).strip()
    try:
        tree   = ast.parse(expr, mode="eval")
        result = _SafeEval().visit(tree)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Could not calculate '{expression}': {e}"


# ── unit converter ─────────────────────────────────────────────────────────────

_CONVERSIONS = {
    # length
    ("km",  "miles"):  lambda x: x * 0.621371,
    ("miles", "km"):   lambda x: x * 1.60934,
    ("m",   "ft"):     lambda x: x * 3.28084,
    ("ft",  "m"):      lambda x: x / 3.28084,
    ("cm",  "inches"): lambda x: x * 0.393701,
    ("inches", "cm"):  lambda x: x / 0.393701,
    # weight
    ("kg",  "lbs"):    lambda x: x * 2.20462,
    ("lbs", "kg"):     lambda x: x / 2.20462,
    ("g",   "oz"):     lambda x: x * 0.035274,
    ("oz",  "g"):      lambda x: x / 0.035274,
    # temperature
    ("c",   "f"):      lambda x: x * 9/5 + 32,
    ("f",   "c"):      lambda x: (x - 32) * 5/9,
    ("c",   "k"):      lambda x: x + 273.15,
    ("k",   "c"):      lambda x: x - 273.15,
    # data
    ("mb",  "gb"):     lambda x: x / 1024,
    ("gb",  "mb"):     lambda x: x * 1024,
    ("gb",  "tb"):     lambda x: x / 1024,
    ("tb",  "gb"):     lambda x: x * 1024,
}

def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    key = (from_unit.lower(), to_unit.lower())
    fn  = _CONVERSIONS.get(key)
    if fn is None:
        return f"Don't know how to convert {from_unit} to {to_unit}."
    result = fn(value)
    return f"{value} {from_unit} = {result:.4f} {to_unit}"
