"""
jarvis/skills/crypto_portfolio.py
Crypto portfolio tracker — JARVIS tracks your crypto holdings,
calculates P&L, and monitors against targets.
"""
import json
import os
import urllib.request
from datetime import datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "crypto_portfolio.json")

_COIN_IDS = {
    "btc": "bitcoin", "bitcoin": "bitcoin",
    "eth": "ethereum", "ethereum": "ethereum",
    "sol": "solana", "solana": "solana",
    "doge": "dogecoin", "dogecoin": "dogecoin",
    "ada": "cardano", "cardano": "cardano",
    "bnb": "binancecoin",
}


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(data: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def _get_price(coin_id: str) -> float | None:
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        return data.get(coin_id, {}).get("usd")
    except Exception:
        return None


def add_holding(coin: str, amount: float, buy_price: float) -> str:
    data    = _load()
    coin_id = _COIN_IDS.get(coin.lower(), coin.lower())
    entry   = {
        "coin":      coin.upper(),
        "coin_id":   coin_id,
        "amount":    amount,
        "buy_price": buy_price,
        "added":     datetime.now().isoformat(),
    }
    data.append(entry)
    _save(data)
    total = amount * buy_price
    return f"Added {amount} {coin.upper()} at ${buy_price:,.2f} (${total:,.2f} total), sir."


def get_portfolio_value() -> str:
    data = _load()
    if not data:
        return "No crypto holdings, sir. Add with 'add crypto holding BTC 0.5 at 45000'."

    total_value    = 0
    total_invested = 0
    lines          = []

    for h in data:
        price = _get_price(h["coin_id"])
        if price is None:
            lines.append(f"{h['coin']}: {h['amount']} (price unavailable)")
            continue
        value    = price * h["amount"]
        invested = h["buy_price"] * h["amount"]
        pl       = value - invested
        pct      = (pl / invested * 100) if invested > 0 else 0
        total_value    += value
        total_invested += invested
        lines.append(
            f"{h['coin']}: {h['amount']} @ ${price:,.2f} = ${value:,.2f} "
            f"(P&L: ${pl:+,.2f} / {pct:+.1f}%)"
        )

    total_pl  = total_value - total_invested
    total_pct = (total_pl / total_invested * 100) if total_invested > 0 else 0

    return (
        f"Crypto portfolio, sir: " +
        " | ".join(lines) +
        f" | TOTAL: ${total_value:,.2f} invested ${total_invested:,.2f} "
        f"P&L ${total_pl:+,.2f} ({total_pct:+.1f}%)."
    )


def clear_portfolio() -> str:
    _save([])
    return "Crypto portfolio cleared, sir."
