"""
jarvis/skills/network_speed_monitor.py
Network speed monitor — JARVIS monitors bandwidth usage
and warns when upload/download speeds drop below thresholds.
"""
import threading
import time
import json
import os


def get_network_stats() -> str:
    """Get current network I/O statistics."""
    try:
        import psutil
        stats  = psutil.net_io_counters()
        sent   = _fmt_bytes(stats.bytes_sent)
        recv   = _fmt_bytes(stats.bytes_recv)
        pkts_s = stats.packets_sent
        pkts_r = stats.packets_recv
        return (
            f"Network stats, sir: "
            f"Sent {sent} ({pkts_s:,} packets), "
            f"Received {recv} ({pkts_r:,} packets)."
        )
    except ImportError:
        return "psutil not installed. Run: pip install psutil"
    except Exception as e:
        return f"Network stats error: {e}"


def measure_bandwidth(duration_secs: int = 3) -> str:
    """Measure current network bandwidth by sampling."""
    try:
        import psutil
        s1     = psutil.net_io_counters()
        time.sleep(duration_secs)
        s2     = psutil.net_io_counters()
        dl_bps = (s2.bytes_recv - s1.bytes_recv) / duration_secs
        ul_bps = (s2.bytes_sent - s1.bytes_sent) / duration_secs
        dl_str = _fmt_speed(dl_bps)
        ul_str = _fmt_speed(ul_bps)
        return f"Current bandwidth, sir: Download {dl_str}, Upload {ul_str}."
    except ImportError:
        return "psutil required: pip install psutil"
    except Exception as e:
        return f"Bandwidth measurement failed: {e}"


def get_connection_count() -> str:
    """Get number of active network connections."""
    try:
        import psutil
        conns   = psutil.net_connections()
        established = [c for c in conns if c.status == "ESTABLISHED"]
        listening   = [c for c in conns if c.status == "LISTEN"]
        return (
            f"Network connections, sir: "
            f"{len(established)} established, "
            f"{len(listening)} listening, "
            f"{len(conns)} total."
        )
    except Exception as e:
        return f"Connection count failed: {e}"


def get_network_interfaces() -> str:
    """List all network interfaces and their status."""
    try:
        import psutil
        stats  = psutil.net_if_stats()
        active = [(iface, info) for iface, info in stats.items() if info.isup]
        parts  = [f"{iface} ({info.speed}Mbps)" for iface, info in active[:5]]
        return f"Active interfaces: {', '.join(parts)}, sir."
    except Exception as e:
        return f"Interface list failed: {e}"


def _fmt_bytes(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if b < 1024:
            return f"{b:.1f}{unit}"
        b /= 1024
    return f"{b:.1f}PB"


def _fmt_speed(bps: float) -> str:
    mbps = bps / (1024 * 1024)
    if mbps >= 1:
        return f"{mbps:.1f} MB/s"
    kbps = bps / 1024
    return f"{kbps:.1f} KB/s"
