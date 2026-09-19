"""Financial feasibility calculator + what-if scenarios."""

from __future__ import annotations


def _safe_div(a, b):
    if b == 0: return 0.0
    v = a / b
    if v != v or v in (float("inf"), float("-inf")): return 0.0
    return float(v)


def financial_analysis(initial_investment, selling_price, units_per_month, monthly_fixed_cost, variable_cost_per_unit):
    revenue = selling_price * units_per_month
    var_cost = variable_cost_per_unit * units_per_month
    total_cost = monthly_fixed_cost + var_cost
    profit = revenue - total_cost
    annual_profit = profit * 12
    roi = _safe_div(annual_profit, initial_investment) * 100 if initial_investment > 0 else 0.0

    contribution = selling_price - variable_cost_per_unit
    if contribution <= 0:
        be_qty = None
        be_note = "Break-even cannot be calculated because contribution margin is non-positive."
    else:
        be_qty = _safe_div(monthly_fixed_cost, contribution); be_note = ""

    be_revenue = (be_qty * selling_price) if be_qty is not None else None
    payback_months = _safe_div(initial_investment, profit) if profit > 0 else None
    payback_note = "" if payback_months is not None else "Payback cannot be calculated because monthly profit is zero or negative."

    return {"monthly_revenue": round(revenue, 2), "variable_cost": round(var_cost, 2),
            "total_monthly_cost": round(total_cost, 2), "monthly_profit": round(profit, 2),
            "annual_profit": round(annual_profit, 2), "roi_percent": round(roi, 2),
            "break_even_quantity": round(be_qty, 2) if be_qty is not None else None,
            "break_even_revenue": round(be_revenue, 2) if be_revenue is not None else None,
            "payback_period_months": round(payback_months, 2) if payback_months is not None else None,
            "break_even_note": be_note, "payback_note": payback_note,
            "assumptions_note": "Financial analysis is based on user assumptions."}


def what_if_analysis(base):
    def scenario(mp, mu, mf, mv):
        return financial_analysis(
            initial_investment=base["initial_investment"],
            selling_price=base["selling_price_per_unit"] * mp,
            units_per_month=base["units_per_month"] * mu,
            monthly_fixed_cost=base["monthly_fixed_cost"] * mf,
            variable_cost_per_unit=base["variable_cost_per_unit"] * mv)

    return {
        "conservative": {"label": "Conservative", "assumptions": {"price": 0.9, "units": 0.8, "fixed": 1.05, "variable": 1.05}, "results": scenario(0.9, 0.8, 1.05, 1.05)},
        "expected": {"label": "Expected", "assumptions": {"price": 1.0, "units": 1.0, "fixed": 1.0, "variable": 1.0}, "results": scenario(1.0, 1.0, 1.0, 1.0)},
        "optimistic": {"label": "Optimistic", "assumptions": {"price": 1.1, "units": 1.2, "fixed": 0.95, "variable": 0.95}, "results": scenario(1.1, 1.2, 0.95, 0.95)},
        "note": "These are scenario-based assumptions, not guaranteed predictions."}
