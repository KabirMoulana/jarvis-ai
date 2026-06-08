"""
jarvis/skills/currency_news.py
Currency and forex news — JARVIS tracks exchange rate
movements and gives financial context.
"""
import urllib.request
import json
from datetime import datetime


_PAIRS = {
    "usd/gbp": ("USD", "GBP"),
    "usd/eur": ("USD", "EUR"),
    "usd/jpy": ("USD", "JPY"),
    "usd/inr": ("USD", "INR"),
    "gbp/eur": ("GBP", "EUR"),
    "eur/jpy": ("EUR", "JPY"),
    "usd/aud": ("USD", "AUD"),
    "usd/cad": ("USD", "CAD"),
    "usd/chf": ("USD", "CHF"),
    "usd/sgd": ("USD", "SGD"),
}

_API = "https://api.frankfurter.app"


def get_rate(from_cur: str, to_cur: str) -> str:
    """Get current exchange rate between two currencies."""
    try:
        url = f"{_API}/latest?from={from_cur.upper()}&to={to_cur.upper()}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        rate = data["rates"].get(to_cur.upper())
        if rate is None:
            return f"Rate for {from_cur}/{to_cur} not available, sir."
        return (
            f"1 {from_cur.upper()} = {rate:.4f} {to_cur.upper()}, sir. "
            f"Rate as of {data['date']}."
        )
    except Exception as e:
        return f"Could not fetch rate: {e}"


def get_rate_history(from_cur: str, to_cur: str, days: int = 7) -> str:
    """Get exchange rate trend over past N days."""
    from datetime import date, timedelta
    try:
        start = (date.today() - timedelta(days=days)).isoformat()
        end   = date.today().isoformat()
        url   = f"{_API}/{start}..{end}?from={from_cur.upper()}&to={to_cur.upper()}"
        req   = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data  = json.loads(resp.read())
        rates = data.get("rates", {})
        if not rates:
            return f"No history available for {from_cur}/{to_cur}, sir."
        values     = [v[to_cur.upper()] for v in rates.values() if to_cur.upper() in v]
        if len(values) < 2:
            return f"Insufficient data for {from_cur}/{to_cur} trend, sir."
        first, last = values[0], values[-1]
        change      = ((last - first) / first) * 100
        direction   = "strengthened" if change > 0 else "weakened"
        return (
            f"{from_cur.upper()}/{to_cur.upper()} {direction} by {abs(change):.2f}% "
            f"over the past {days} days, sir. "
            f"Range: {min(values):.4f} to {max(values):.4f}."
        )
    except Exception as e:
        return f"History fetch failed: {e}"


def get_major_rates() -> str:
    """Get a snapshot of major currency pairs."""
    pairs   = [("USD", "EUR"), ("USD", "GBP"), ("USD", "JPY"), ("USD", "INR")]
    results = []
    for f, t in pairs:
        try:
            url = f"{_API}/latest?from={f}&to={t}"
            req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
            rate = data["rates"].get(t, 0)
            results.append(f"{f}/{t}: {rate:.4f}")
        except Exception:
            pass
    if not results:
        return "Currency data unavailable, sir."
    return "Major rates, sir: " + " | ".join(results) + "."
