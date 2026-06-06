"""
jarvis/skills/investment_calculator.py
Investment calculator — JARVIS calculates compound interest,
ROI, mortgage payments, and retirement projections.
"""
import math


def compound_interest(principal: float, rate_pct: float,
                      years: int, compounds_per_year: int = 12) -> str:
    """Calculate compound interest."""
    r      = rate_pct / 100
    n      = compounds_per_year
    amount = principal * (1 + r/n) ** (n * years)
    gained = amount - principal
    return (
        f"Compound interest on ${principal:,.2f} at {rate_pct}% for {years} years, sir: "
        f"Final value: ${amount:,.2f}. "
        f"Interest earned: ${gained:,.2f}."
    )


def roi(initial: float, final: float) -> str:
    """Calculate return on investment."""
    if initial <= 0:
        return "Initial investment must be greater than zero, sir."
    roi_pct = ((final - initial) / initial) * 100
    gain    = final - initial
    return (
        f"ROI: {roi_pct:.2f}% on ${initial:,.2f} investment. "
        f"Gain: ${gain:+,.2f}. Final value: ${final:,.2f}, sir."
    )


def mortgage_payment(principal: float, annual_rate_pct: float,
                     years: int) -> str:
    """Calculate monthly mortgage payment."""
    r = annual_rate_pct / 100 / 12
    n = years * 12
    if r == 0:
        monthly = principal / n
    else:
        monthly = principal * (r * (1 + r)**n) / ((1 + r)**n - 1)
    total    = monthly * n
    interest = total - principal
    return (
        f"Mortgage on ${principal:,.2f} at {annual_rate_pct}% for {years} years, sir: "
        f"Monthly payment: ${monthly:,.2f}. "
        f"Total paid: ${total:,.2f}. "
        f"Total interest: ${interest:,.2f}."
    )


def retirement_projection(monthly_contribution: float,
                           annual_return_pct: float,
                           years: int,
                           current_savings: float = 0) -> str:
    """Project retirement savings."""
    r       = annual_return_pct / 100 / 12
    n       = years * 12
    # Future value of regular contributions (annuity)
    if r > 0:
        fv_contributions = monthly_contribution * ((1 + r)**n - 1) / r
    else:
        fv_contributions = monthly_contribution * n
    # Future value of current savings
    fv_savings = current_savings * (1 + r)**n
    total      = fv_contributions + fv_savings
    invested   = monthly_contribution * n + current_savings
    growth     = total - invested
    return (
        f"Retirement projection, sir: "
        f"Contributing ${monthly_contribution:,.2f}/month for {years} years "
        f"at {annual_return_pct}% return. "
        f"Projected value: ${total:,.2f}. "
        f"Total invested: ${invested:,.2f}. "
        f"Investment growth: ${growth:,.2f}."
    )


def rule_of_72(rate_pct: float) -> str:
    """Calculate years to double investment."""
    years = 72 / rate_pct
    return (
        f"At {rate_pct}% annual return, your investment doubles every "
        f"{years:.1f} years (Rule of 72), sir."
    )


def break_even(fixed_costs: float, price_per_unit: float,
               variable_cost_per_unit: float) -> str:
    """Calculate break-even point."""
    if price_per_unit <= variable_cost_per_unit:
        return "Price must exceed variable cost to break even, sir."
    units  = fixed_costs / (price_per_unit - variable_cost_per_unit)
    revenue = units * price_per_unit
    return (
        f"Break-even point, sir: {units:,.0f} units / ${revenue:,.2f} revenue. "
        f"Above this, you're profitable."
    )
