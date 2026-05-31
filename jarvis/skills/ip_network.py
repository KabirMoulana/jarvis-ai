"""
jarvis/skills/ip_network.py
Network diagnostics skill — IP address, ping, network interfaces.
Gives JARVIS-style spoken reports on network status.
"""
import socket
import subprocess
import sys
import urllib.request
import json


def get_local_ip() -> str:
    """Return the local network IP address."""
    try:
        # Connect to an external address to find the right interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"Your local IP address is {ip}, sir."
    except Exception:
        return "Unable to determine local IP address."


def get_public_ip() -> str:
    """Return the public-facing IP address."""
    try:
        req = urllib.request.Request(
            "https://api.ipify.org?format=json",
            headers={"User-Agent": "JarvisAI/3.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        ip = data.get("ip", "unknown")
        return f"Your public IP address is {ip}, sir."
    except Exception:
        return "Could not retrieve public IP. You may be offline, sir."


def ping_host(host: str) -> str:
    """Ping a host and return latency info."""
    host = host.strip().replace("https://", "").replace("http://", "").split("/")[0]
    flag = "-c" if sys.platform != "win32" else "-n"
    try:
        result = subprocess.run(
            ["ping", flag, "3", host],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            # Try to parse average latency from ping output
            output = result.stdout
            for line in output.split("\n"):
                if "avg" in line.lower() or "average" in line.lower():
                    return f"{host} is reachable, sir. {line.strip()}"
            return f"{host} is reachable, sir."
        else:
            return f"{host} is not responding, sir. It may be offline."
    except subprocess.TimeoutExpired:
        return f"Ping to {host} timed out, sir."
    except Exception as e:
        return f"Ping failed: {e}"


def check_internet() -> str:
    """Quick check if internet is available."""
    try:
        urllib.request.urlopen("https://www.google.com", timeout=4)
        return "Internet connection is active, sir."
    except Exception:
        return "No internet connection detected, sir."
