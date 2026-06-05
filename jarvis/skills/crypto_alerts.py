"""
jarvis/skills/crypto_alerts.py
Crypto price alerts — JARVIS monitors crypto prices and
alerts you when targets are hit.
"""
import threading
import time
import json
import os
import urllib.request

_FILE    = os.path.join(os.path.dirname(__file__), "..", "memory", "crypto_alerts.json")
_running = False
_thread  = None


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
        json.dump(data, f, indent=2)


def add_alert(coin: str, target_price: float,
              condition: str = "above", callback=None) -> str:
    """Add a price alert. condition: 'above' or 'below'."""
    data = _load()
    alert = {
        "id":        len(data) + 1,
        "coin":      coin.lower(),
        "target":    target_price,
        "condition": condition.lower(),
        "triggered": False,
        "callback":  None,
    }
    data.append(alert)
    _save(data)
    return (
        f"Alert set: notify when {coin.upper()} goes "
        f"{'above' if condition == 'above' else 'below'} "
        f"${target_price:,.2f}, sir."
    )


def start_monitoring(callback=None) -> str:
    global _running, _thread
    if _running:
        return "Crypto monitoring already active, sir."
    _running = True

    def _loop():
        while _running:
            _check_alerts(callback)
            time.sleep(60)  # Check every minute

    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()
    return "Crypto price monitoring started, sir. Checking every minute."


def stop_monitoring() -> str:
    global _running
    _running = False
    return "Crypto monitoring stopped, sir."


def _check_alerts(callback=None):
    data     = _load()
    modified = False
    for alert in data:
        if alert["triggered"]:
            continue
        try:
            price = _get_price(alert["coin"])
            if price is None:
                continue
            hit = (alert["condition"] == "above" and price >= alert["target"]) or \
                  (alert["condition"] == "below" and price <= alert["target"])
            if hit:
                alert["triggered"] = True
                modified = True
                msg = (
                    f"Crypto alert! {alert['coin'].upper()} is now "
                    f"${price:,.2f} — "
                    f"{'above' if alert['condition'] == 'above' else 'below'} "
                    f"your ${alert['target']:,.2f} target, sir."
                )
                print(f"\n🚨  {msg}")
                if callback:
                    callback(msg)
        except Exception:
            pass
    if modified:
        _save(data)


def _get_price(coin: str) -> float | None:
    _COIN_IDS = {
        "bitcoin": "bitcoin", "btc": "bitcoin",
        "ethereum": "ethereum", "eth": "ethereum",
        "solana": "solana", "sol": "solana",
        "doge": "dogecoin", "dogecoin": "dogecoin",
    }
    coin_id = _COIN_IDS.get(coin.lower(), coin.lower())
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        return data.get(coin_id, {}).get("usd")
    except Exception:
        return None


def list_alerts() -> str:
    data    = _load()
    pending = [a for a in data if not a["triggered"]]
    if not pending:
        return "No active crypto alerts, sir."
    parts = [
        f"{a['id']}. {a['coin'].upper()} "
        f"{'>' if a['condition'] == 'above' else '<'} "
        f"${a['target']:,.2f}"
        for a in pending
    ]
    return f"{len(pending)} active alert(s): " + " | ".join(parts) + ", sir."
