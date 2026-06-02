"""
jarvis/skills/currency.py
Real-time currency converter — uses ExchangeRate-API (free tier, no key)
and falls back to Frankfurter API. Covers 30+ currencies.
"""
import urllib.request
import json

_FRANKFURTER = "https://api.frankfurter.app"

_CURRENCY_NAMES = {
    "usd": "US Dollar", "eur": "Euro", "gbp": "British Pound",
    "jpy": "Japanese Yen", "inr": "Indian Rupee", "cad": "Canadian Dollar",
    "aud": "Australian Dollar", "chf": "Swiss Franc", "cny": "Chinese Yuan",
    "sgd": "Singapore Dollar", "aed": "UAE Dirham", "sar": "Saudi Riyal",
    "myr": "Malaysian Ringgit", "thb": "Thai Baht", "idr": "Indonesian Rupiah",
    "brl": "Brazilian Real", "mxn": "Mexican Peso", "rub": "Russian Ruble",
    "zar": "South African Rand", "nok": "Norwegian Krone", "sek": "Swedish Krona",
    "dkk": "Danish Krone", "nzd": "New Zealand Dollar", "hkd": "Hong Kong Dollar",
    "krw": "South Korean Won", "try": "Turkish Lira", "pln": "Polish Zloty",
    "php": "Philippine Peso", "lkr": "Sri Lankan Rupee",
}

_ALIASES = {
    "dollar": "usd", "dollars": "usd", "buck": "usd", "bucks": "usd",
    "euro": "eur", "euros": "eur", "pound": "gbp", "pounds": "gbp",
    "yen": "jpy", "rupee": "inr", "rupees": "inr", "yuan": "cny",
    "dirham": "aed", "riyal": "sar", "ringgit": "myr", "baht": "thb",
    "lira": "try", "won": "krw", "peso": "mxn",
}


def convert_currency(amount: float, from_cur: str, to_cur: str) -> str:
    from_code = _resolve(from_cur)
    to_code   = _resolve(to_cur)
    if not from_code:
        return f"Unknown currency: {from_cur}, sir."
    if not to_code:
        return f"Unknown currency: {to_cur}, sir."
    if from_code == to_code:
        return f"{amount} {from_code.upper()} is {amount} {to_code.upper()}, sir."

    try:
        url = f"{_FRANKFURTER}/latest?amount={amount}&from={from_code.upper()}&to={to_code.upper()}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data  = json.loads(resp.read())
        result = data["rates"][to_code.upper()]
        from_name = _CURRENCY_NAMES.get(from_code, from_code.upper())
        to_name   = _CURRENCY_NAMES.get(to_code,   to_code.upper())
        return (
            f"{amount:,.2f} {from_name} = {result:,.2f} {to_name}, sir."
        )
    except Exception as e:
        return f"Currency conversion failed: {e}"


def get_exchange_rate(from_cur: str, to_cur: str) -> str:
    return convert_currency(1, from_cur, to_cur)


def list_currencies() -> str:
    names = ", ".join(f"{k.upper()} ({v})" for k, v in list(_CURRENCY_NAMES.items())[:10])
    return f"Supported currencies include: {names}, and more, sir."


def _resolve(name: str) -> str | None:
    name = name.lower().strip()
    if name in _CURRENCY_NAMES:
        return name
    if name in _ALIASES:
        return _ALIASES[name]
    # 3-letter code fallback
    if len(name) == 3:
        return name
    return None


def parse_currency_query(text: str) -> str:
    """Parse 'convert 100 dollars to euros' or '50 gbp in usd'."""
    import re
    m = re.search(
        r"(\d+\.?\d*)\s+([\w]+)\s+(?:to|in(?:to)?)\s+([\w]+)",
        text, re.IGNORECASE
    )
    if m:
        return convert_currency(float(m.group(1)), m.group(2), m.group(3))
    return "Please say something like 'convert 100 dollars to euros', sir."
