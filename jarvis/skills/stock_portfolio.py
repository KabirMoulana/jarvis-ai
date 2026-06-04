"""
jarvis/skills/stock_portfolio.py
Stock portfolio tracker — JARVIS tracks your investments.
Add stocks, track P&L, get alerts on price targets.
"""
import json
import os
from datetime import datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "portfolio.json")


def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"holdings": [], "watchlist": []}


def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def add_holding(ticker: str, shares: float, buy_price: float) -> str:
    data = _load()
    ticker = ticker.upper().strip()
    holding = {
        "ticker":    ticker,
        "shares":    shares,
        "buy_price": buy_price,
        "added":     datetime.now().isoformat(),
    }
    data["holdings"].append(holding)
    _save(data)
    total = shares * buy_price
    return f"Added {shares} shares of {ticker} at ${buy_price:.2f} (${total:,.2f} total), sir."


def get_portfolio_summary() -> str:
    data     = _load()
    holdings = data["holdings"]
    if not holdings:
        return "No holdings in portfolio, sir. Say 'add holding AAPL 10 shares at 150' to start."

    try:
        from jarvis.skills.crypto_stocks import _get_stock_fallback
        lines    = []
        total_pl = 0
        for h in holdings:
            try:
                result   = _get_stock_fallback(h["ticker"])
                import re
                price_m  = re.search(r"\$(\d+\.?\d*)", result)
                cur_price = float(price_m.group(1)) if price_m else h["buy_price"]
                pl        = (cur_price - h["buy_price"]) * h["shares"]
                total_pl += pl
                pct       = (cur_price - h["buy_price"]) / h["buy_price"] * 100
                lines.append(
                    f"{h['ticker']}: {h['shares']} shares, "
                    f"P&L ${pl:+.2f} ({pct:+.1f}%)"
                )
            except Exception:
                lines.append(f"{h['ticker']}: {h['shares']} shares (price unavailable)")
        summary = ". ".join(lines)
        return f"Portfolio summary, sir. {summary}. Total P&L: ${total_pl:+.2f}."
    except Exception:
        tickers = ", ".join(h["ticker"] for h in holdings)
        return f"Holdings: {tickers}, sir. Install yfinance for live P&L."


def add_to_watchlist(ticker: str, target_price: float = 0) -> str:
    data   = _load()
    ticker = ticker.upper().strip()
    data["watchlist"].append({"ticker": ticker, "target": target_price})
    _save(data)
    msg = f"${target_price:.2f} target" if target_price else "no target set"
    return f"{ticker} added to watchlist ({msg}), sir."


def get_watchlist() -> str:
    data = _load()
    wl   = data.get("watchlist", [])
    if not wl:
        return "Watchlist is empty, sir."
    items = [f"{w['ticker']}" + (f" (target ${w['target']:.2f})" if w.get("target") else "") for w in wl]
    return "Watchlist: " + ", ".join(items) + ", sir."
