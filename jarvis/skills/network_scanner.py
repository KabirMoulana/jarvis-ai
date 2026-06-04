"""
jarvis/skills/network_scanner.py
Network scanner — JARVIS scans the local network for connected devices.
Uses ARP and socket scanning. Requires: pip install scapy (optional)
"""
import socket
import subprocess
import sys
import re
import os


def get_local_network_info() -> str:
    """Get local network interface information."""
    try:
        import psutil
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        parts = []
        for iface, addr_list in addrs.items():
            if not stats[iface].isup:
                continue
            for addr in addr_list:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    parts.append(f"{iface}: {addr.address}/{addr.netmask}")
        if not parts:
            return "No active network interfaces found, sir."
        return "Network interfaces: " + ", ".join(parts) + ", sir."
    except ImportError:
        return _fallback_ip_info()


def _fallback_ip_info() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"Local IP: {ip}, sir."
    except Exception as e:
        return f"Network info unavailable: {e}"


def scan_local_devices(subnet: str = "") -> str:
    """Scan for active devices on the local network using ping sweep."""
    if not subnet:
        # Auto-detect subnet
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            parts  = ip.split(".")
            subnet = ".".join(parts[:3]) + "."
        except Exception:
            return "Could not determine local subnet, sir."

    live_hosts = []
    flag       = "-c" if sys.platform != "win32" else "-n"

    # Scan first 20 hosts only — quick scan
    import threading
    def ping(host):
        result = subprocess.run(
            ["ping", flag, "1", "-W", "1", host],
            capture_output=True, timeout=2
        )
        if result.returncode == 0:
            live_hosts.append(host)

    threads = []
    for i in range(1, 21):
        host = f"{subnet}{i}"
        t    = threading.Thread(target=ping, args=(host,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=3)

    if not live_hosts:
        return "No devices found on local network, sir."
    return f"Found {len(live_hosts)} active device(s) on {subnet}0/24: " + ", ".join(live_hosts) + "."


def dns_lookup(domain: str) -> str:
    """Perform a DNS lookup for a domain."""
    try:
        ip = socket.gethostbyname(domain)
        return f"DNS lookup: {domain} resolves to {ip}, sir."
    except socket.gaierror:
        return f"Could not resolve {domain}, sir. It may not exist."


def reverse_dns(ip: str) -> str:
    """Reverse DNS lookup — IP to hostname."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return f"Reverse DNS: {ip} is {hostname}, sir."
    except Exception:
        return f"No reverse DNS entry found for {ip}, sir."


def check_port(host: str, port: int) -> str:
    """Check if a specific port is open on a host."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex((host, port))
        s.close()
        if result == 0:
            return f"Port {port} is open on {host}, sir."
        return f"Port {port} is closed on {host}, sir."
    except Exception as e:
        return f"Port check failed: {e}"
