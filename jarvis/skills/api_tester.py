"""
jarvis/skills/api_tester.py
API tester — JARVIS sends HTTP requests and reports results.
GET, POST, headers, response time. Developer utility.
"""
import urllib.request
import urllib.error
import json
import time


def get_request(url: str, headers: dict | None = None) -> str:
    """Send a GET request and return a summary."""
    h = {"User-Agent": "JarvisAI/3.0"}
    if headers:
        h.update(headers)
    try:
        req   = urllib.request.Request(url, headers=h)
        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed = (time.time() - start) * 1000
            status  = resp.status
            body    = resp.read().decode("utf-8", errors="replace")
        preview = body[:200].replace("\n", " ").strip()
        return (
            f"GET {url} — Status {status}, "
            f"{elapsed:.0f}ms. "
            f"Response: {preview}{'...' if len(body) > 200 else ''}, sir."
        )
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code} error from {url}, sir."
    except Exception as e:
        return f"Request failed: {e}"


def post_request(url: str, data: dict, headers: dict | None = None) -> str:
    """Send a POST request with JSON body."""
    h = {"User-Agent": "JarvisAI/3.0", "Content-Type": "application/json"}
    if headers:
        h.update(headers)
    try:
        payload = json.dumps(data).encode()
        req     = urllib.request.Request(url, data=payload, headers=h, method="POST")
        start   = time.time()
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed = (time.time() - start) * 1000
            status  = resp.status
            body    = resp.read().decode("utf-8", errors="replace")
        return f"POST {url} — Status {status}, {elapsed:.0f}ms, sir."
    except Exception as e:
        return f"POST failed: {e}"


def check_api_status(url: str) -> str:
    """Quick check if an API endpoint is reachable."""
    try:
        req   = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=5) as resp:
            ms = (time.time() - start) * 1000
        return f"{url} is up — {resp.status}, {ms:.0f}ms, sir."
    except urllib.error.HTTPError as e:
        return f"{url} returned HTTP {e.code}, sir."
    except Exception:
        return f"{url} is unreachable, sir."


def parse_json_response(url: str, key_path: str = "") -> str:
    """Fetch JSON from URL and extract a value by dot-notation key."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        if key_path:
            for key in key_path.split("."):
                data = data[key]
        return f"Value at '{key_path}': {str(data)[:200]}, sir."
    except KeyError:
        return f"Key '{key_path}' not found in response, sir."
    except Exception as e:
        return f"JSON parse failed: {e}"
