"""
jarvis/skills/vitals.py
System vitals — CPU, RAM, disk, battery, uptime.
Returns JARVIS-style spoken summaries.
Requires: psutil  (pip install psutil)
"""
import platform
import datetime

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False


def get_vitals() -> str:
    """Return a full system vitals report in JARVIS style."""
    if not _HAS_PSUTIL:
        return "System monitoring unavailable, sir. The psutil library is not installed."

    cpu   = psutil.cpu_percent(interval=0.5)
    ram   = psutil.virtual_memory()
    disk  = psutil.disk_usage("/")
    up    = _uptime()

    parts = [
        f"CPU at {cpu:.0f} percent",
        f"RAM usage {ram.percent:.0f} percent — {_fmt(ram.used)} of {_fmt(ram.total)} used",
        f"Disk at {disk.percent:.0f} percent capacity",
        f"System uptime {up}",
    ]

    battery = _battery()
    if battery:
        parts.append(battery)

    return ". ".join(parts) + "."


def get_cpu() -> str:
    if not _HAS_PSUTIL:
        return "CPU data unavailable."
    return f"CPU is running at {psutil.cpu_percent(interval=0.5):.0f} percent, {_core_count()} cores."


def get_ram() -> str:
    if not _HAS_PSUTIL:
        return "Memory data unavailable."
    m = psutil.virtual_memory()
    return (
        f"Memory: {_fmt(m.used)} used of {_fmt(m.total)} total — "
        f"{m.percent:.0f} percent in use, {_fmt(m.available)} available."
    )


def get_battery() -> str:
    if not _HAS_PSUTIL:
        return "Battery data unavailable."
    b = _battery()
    return b if b else "No battery detected — running on mains power, sir."


# ── helpers ───────────────────────────────────────────────────────────────────

def _fmt(bytes_val: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def _uptime() -> str:
    try:
        boot   = psutil.boot_time()
        now    = datetime.datetime.now().timestamp()
        delta  = int(now - boot)
        hours, rem = divmod(delta, 3600)
        mins, _    = divmod(rem, 60)
        return f"{hours} hours {mins} minutes"
    except Exception:
        return "unknown"


def _battery() -> str | None:
    try:
        b = psutil.sensors_battery()
        if b is None:
            return None
        status = "charging" if b.power_plugged else "on battery"
        return f"Battery at {b.percent:.0f} percent, {status}"
    except Exception:
        return None


def _core_count() -> str:
    try:
        physical = psutil.cpu_count(logical=False) or "?"
        logical  = psutil.cpu_count(logical=True)  or "?"
        return f"{physical} physical, {logical} logical"
    except Exception:
        return "unknown"
