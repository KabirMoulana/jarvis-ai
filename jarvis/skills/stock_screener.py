"""
jarvis/skills/stock_screener.py
Stock screener — JARVIS filters stocks by criteria
like sector, performance, and market cap.
Uses Yahoo Finance fallback for public data.
"""
import urllib.request
import json


_POPULAR_STOCKS = {
    "tech":    ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "AMD", "INTC", "TSLA"],
    "finance": ["JPM", "BAC", "WFC", "GS", "MS", "V", "MA", "AXP"],
    "energy":  ["XOM", "CVX", "BP", "SHEL", "COP", "SLB", "EOG"],
    "health":  ["JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT"],
    "consumer":["AMZN", "WMT", "HD", "NKE", "MCD", "SBUX", "PG"],
    "crypto_related": ["COIN", "MARA", "RIOT", "MSTR", "CLSK"],
}


def _get_price(ticker: str) -> dict | None:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=2d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        meta   = data["chart"]["result"][0]["meta"]
        price  = meta["regularMarketPrice"]
        prev   = meta["previousClose"]
        change = ((price - prev) / prev * 100) if prev else 0
        return {"ticker": ticker, "price": price, "change": change}
    except Exception:
        return None


def screen_sector(sector: str, top_n: int = 3) -> str:
    """Get top movers in a sector."""
    sector  = sector.lower()
    tickers = None
    for key in _POPULAR_STOCKS:
        if sector in key or key in sector:
            tickers = _POPULAR_STOCKS[key]
            break
    if not tickers:
        sectors = ", ".join(_POPULAR_STOCKS.keys())
        return f"Sector '{sector}' not found, sir. Available: {sectors}."

    results = []
    for t in tickers[:6]:
        data = _get_price(t)
        if data:
            results.append(data)

    if not results:
        return f"Could not fetch {sector} stock data, sir."

    results.sort(key=lambda x: x["change"], reverse=True)
    parts = [
        f"{r['ticker']} ${r['price']:.2f} ({r['change']:+.1f}%)"
        for r in results[:top_n]
    ]
    return f"Top {sector} stocks, sir: " + " | ".join(parts) + "."


def get_market_movers() -> str:
    """Get today's biggest movers across sectors."""
    movers = []
    for sector, tickers in list(_POPULAR_STOCKS.items())[:3]:
        for t in tickers[:2]:
            data = _get_price(t)
            if data:
                movers.append(data)

    if not movers:
        return "Market data unavailable, sir."

    movers.sort(key=lambda x: abs(x["change"]), reverse=True)
    top = movers[:5]
    parts = [f"{r['ticker']} {r['change']:+.1f}%" for r in top]
    return "Biggest movers today: " + " | ".join(parts) + ", sir."


def compare_stocks(ticker1: str, ticker2: str) -> str:
    """Compare two stocks side by side."""
    d1 = _get_price(ticker1.upper())
    d2 = _get_price(ticker2.upper())
    if not d1 or not d2:
        return "Could not fetch comparison data, sir."
    winner = ticker1 if d1["change"] > d2["change"] else ticker2
    return (
        f"Comparison, sir: "
        f"{ticker1.upper()} ${d1['price']:.2f} ({d1['change']:+.1f}%) vs "
        f"{ticker2.upper()} ${d2['price']:.2f} ({d2['change']:+.1f}%). "
        f"{winner.upper()} is outperforming today."
    )
