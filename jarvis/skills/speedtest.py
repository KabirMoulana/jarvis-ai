"""
jarvis/skills/speedtest.py
Internet speed test — download, upload, and ping.
Uses speedtest-cli if installed, falls back to a lightweight
manual test via HTTP download timing.
Install: pip install speedtest-cli
"""
import urllib.request
import time


def run_speedtest() -> str:
    """Run a full speed test and return JARVIS-style results."""
    # Try speedtest-cli first
    try:
        import speedtest
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()

        print("[Speedtest] Testing download ...")
        download = st.download() / 1_000_000   # Mbps

        print("[Speedtest] Testing upload ...")
        upload   = st.upload() / 1_000_000     # Mbps

        ping     = st.results.ping
        server   = st.results.server.get("name", "unknown")

        return (
            f"Speed test complete, sir. "
            f"Download: {download:.1f} Mbps. "
            f"Upload: {upload:.1f} Mbps. "
            f"Ping: {ping:.0f} milliseconds via {server}."
        )
    except ImportError:
        pass
    except Exception as e:
        return f"Speed test failed: {e}"

    # Fallback: manual download timing
    return _manual_download_test()


def _manual_download_test() -> str:
    """Estimate download speed by timing a ~10MB file download."""
    test_url = "http://speed.cloudflare.com/__down?bytes=10000000"
    try:
        req   = urllib.request.Request(test_url, headers={"User-Agent": "JarvisAI/3.0"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        elapsed  = time.time() - start
        mbps     = (len(data) * 8) / (elapsed * 1_000_000)
        ping_ms  = _quick_ping()
        return (
            f"Estimated download speed: {mbps:.1f} Mbps, sir. "
            f"Ping: {ping_ms} milliseconds. "
            f"For full upload results, install speedtest-cli."
        )
    except Exception as e:
        return f"Speed test unavailable: {e}"


def _quick_ping() -> int:
    """Measure rough latency to Cloudflare DNS."""
    try:
        start = time.time()
        urllib.request.urlopen("http://1.1.1.1", timeout=3)
        return int((time.time() - start) * 1000)
    except Exception:
        return -1


def get_ping(host: str = "1.1.1.1") -> str:
    ms = _quick_ping()
    if ms < 0:
        return f"Could not reach {host}, sir."
    return f"Ping to {host}: {ms} milliseconds, sir."
