"""
jarvis/skills/crypto_stocks.py
Real-time crypto and stock prices — no API key required.
Uses Yahoo Finance (yfinance) for stocks and CoinGecko for crypto.
"""
import urllib.request
import json


# ── Crypto (CoinGecko — free, no key) ────────────────────────────────────────
_COINGECKO = "https://api.coingecko.com/api/v3"

_COIN_IDS = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "cardano": "cardano", "ada": "cardano",
    "ripple": "ripple", "xrp": "ripple",
    "bnb": "binancecoin", "binance": "binancecoin",
}


def get_crypto_price(coin: str, currency: str = "usd") -> str:
    coin_id = _COIN_IDS.get(coin.lower().strip(), coin.lower().strip())
    try:
        url = f"{_COINGECKO}/simple/price?ids={coin_id}&vs_currencies={currency}&include_24hr_change=true"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        if coin_id not in data:
            return f"Could not find price for {coin}, sir."
        price  = data[coin_id][currency]
        change = data[coin_id].get(f"{currency}_24h_change", 0)
        arrow  = "up" if change >= 0 else "down"
        return (
            f"{coin.capitalize()} is trading at "
            f"{'${:,.2f}'.format(price)} {currency.upper()}, "
            f"{arrow} {abs(change):.1f} percent in the last 24 hours, sir."
        )
    except Exception as e:
        return f"Could not retrieve {coin} price: {e}"


# ── Stocks (yfinance — pip install yfinance) ──────────────────────────────────
def get_stock_price(ticker: str) -> str:
    ticker = ticker.upper().strip()
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        info  = stock.fast_info
        price = info.last_price
        prev  = info.previous_close
        change = ((price - prev) / prev * 100) if prev else 0
        arrow  = "up" if change >= 0 else "down"
        return (
            f"{ticker} is trading at ${price:.2f}, "
            f"{arrow} {abs(change):.1f} percent today, sir."
        )
    except ImportError:
        return _get_stock_fallback(ticker)
    except Exception as e:
        return f"Could not retrieve {ticker} price: {e}"


def _get_stock_fallback(ticker: str) -> str:
    """Fallback using Yahoo Finance JSON API."""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=2d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
        meta  = data["chart"]["result"][0]["meta"]
        price = meta["regularMarketPrice"]
        prev  = meta["previousClose"]
        change = ((price - prev) / prev * 100) if prev else 0
        arrow  = "up" if change >= 0 else "down"
        return (
            f"{ticker} is trading at ${price:.2f}, "
            f"{arrow} {abs(change):.1f} percent today, sir."
        )
    except Exception as e:
        return f"Could not retrieve {ticker}: {e}"


def get_market_summary() -> str:
    """Quick summary of major indices."""
    tickers = [("^GSPC", "S&P 500"), ("^DJI", "Dow Jones"), ("^IXIC", "Nasdaq")]
    parts   = []
    for symbol, name in tickers:
        try:
            result = _get_stock_fallback(symbol)
            # Strip the "sir." and replace ticker with name
            result = result.replace(symbol, name).rstrip(".")
            parts.append(result)
        except Exception:
            pass
    if not parts:
        return "Market data unavailable at this time, sir."
    return " ".join(parts) + "."
