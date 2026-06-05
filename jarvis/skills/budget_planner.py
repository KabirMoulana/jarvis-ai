"""
jarvis/skills/budget_planner.py
Budget planner — JARVIS helps plan monthly budgets
using the 50/30/20 rule and custom allocations.
"""
import json
import os
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "budget.json")


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_budget_50_30_20(income: float) -> str:
    """Create a budget using the 50/30/20 rule."""
    needs   = income * 0.50
    wants   = income * 0.30
    savings = income * 0.20
    data = {
        "income":   income,
        "needs":    needs,
        "wants":    wants,
        "savings":  savings,
        "created":  str(date.today()),
        "rule":     "50/30/20",
    }
    _save(data)
    return (
        f"Budget created for ${income:,.2f}/month, sir. "
        f"Needs (50%): ${needs:,.2f}. "
        f"Wants (30%): ${wants:,.2f}. "
        f"Savings (20%): ${savings:,.2f}."
    )


def create_custom_budget(income: float, needs_pct: int,
                         wants_pct: int, savings_pct: int) -> str:
    total = needs_pct + wants_pct + savings_pct
    if total != 100:
        return f"Percentages must add up to 100%, sir. Yours total {total}%."
    needs   = income * needs_pct / 100
    wants   = income * wants_pct / 100
    savings = income * savings_pct / 100
    data = {
        "income":  income, "needs": needs,
        "wants":   wants,  "savings": savings,
        "created": str(date.today()),
        "rule":    f"{needs_pct}/{wants_pct}/{savings_pct}",
    }
    _save(data)
    return (
        f"Custom budget set, sir. "
        f"Needs ({needs_pct}%): ${needs:,.2f}. "
        f"Wants ({wants_pct}%): ${wants:,.2f}. "
        f"Savings ({savings_pct}%): ${savings:,.2f}."
    )


def get_budget() -> str:
    data = _load()
    if not data:
        return "No budget set, sir. Say 'create budget 5000' to start."
    return (
        f"Current budget (${data['income']:,.2f}/month, {data['rule']} rule), sir: "
        f"Needs ${data['needs']:,.2f} | "
        f"Wants ${data['wants']:,.2f} | "
        f"Savings ${data['savings']:,.2f}."
    )


def savings_goal(target: float, monthly_savings: float) -> str:
    """Calculate how long to reach a savings goal."""
    if monthly_savings <= 0:
        return "Monthly savings must be greater than zero, sir."
    months = target / monthly_savings
    years  = months / 12
    return (
        f"To save ${target:,.2f} at ${monthly_savings:,.2f}/month, "
        f"you'll need {months:.0f} months ({years:.1f} years), sir."
    )


def emergency_fund_target(monthly_expenses: float, months: int = 6) -> str:
    target = monthly_expenses * months
    return (
        f"Recommended emergency fund ({months} months of expenses): "
        f"${target:,.2f}, sir. "
        f"At $500/month savings, that's {target/500:.0f} months away."
    )
