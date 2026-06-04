"""
jarvis/skills/system_health.py
System health monitor — JARVIS runs periodic health checks
and alerts when something is wrong (high CPU, low disk, high temp).
"""
import threading
import time
import os


_THRESHOLDS = {
    "cpu_percent":    85.0,
    "ram_percent":    90.0,
    "disk_percent":   90.0,
    "temp_celsius":   80.0,
}

_monitoring    = False
_monitor_thread = None


def run_health_check() -> str:
    """Run a one-time system health check."""
    try:
        import psutil
    except ImportError:
        return "psutil not installed. Run: pip install psutil"

    issues  = []
    reports = []

    cpu = psutil.cpu_percent(interval=1)
    reports.append(f"CPU: {cpu:.0f}%")
    if cpu > _THRESHOLDS["cpu_percent"]:
        issues.append(f"CPU at {cpu:.0f}% — unusually high")

    ram = psutil.virtual_memory().percent
    reports.append(f"RAM: {ram:.0f}%")
    if ram > _THRESHOLDS["ram_percent"]:
        issues.append(f"RAM at {ram:.0f}% — critically high")

    disk = psutil.disk_usage("/").percent
    reports.append(f"Disk: {disk:.0f}%")
    if disk > _THRESHOLDS["disk_percent"]:
        issues.append(f"Disk at {disk:.0f}% — nearly full")

    # Temperature (if available)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            max_temp = max(t.current for readings in temps.values() for t in readings)
            reports.append(f"Temp: {max_temp:.0f}°C")
            if max_temp > _THRESHOLDS["temp_celsius"]:
                issues.append(f"Temperature at {max_temp:.0f}°C — overheating risk")
    except Exception:
        pass

    summary = " | ".join(reports)
    if issues:
        return f"Health check — WARNINGS: {'; '.join(issues)}. Summary: {summary}."
    return f"All systems healthy, sir. {summary}."


def start_monitoring(interval_mins: int = 5, callback=None) -> str:
    """Start periodic health monitoring in the background."""
    global _monitoring, _monitor_thread
    if _monitoring:
        return "Health monitoring already active, sir."
    _monitoring = True

    def _loop():
        while _monitoring:
            time.sleep(interval_mins * 60)
            result = run_health_check()
            if "WARNING" in result:
                msg = f"System alert, sir. {result}"
                print(f"\n⚠️  {msg}")
                if callback:
                    callback(msg)

    _monitor_thread = threading.Thread(target=_loop, daemon=True)
    _monitor_thread.start()
    return f"System health monitoring started, sir. Checking every {interval_mins} minutes."


def stop_monitoring() -> str:
    global _monitoring
    _monitoring = False
    return "Health monitoring stopped, sir."


def get_temperature() -> str:
    """Get current CPU/system temperature."""
    try:
        import psutil
        temps = psutil.sensors_temperatures()
        if not temps:
            return "Temperature sensors not available on this system, sir."
        results = []
        for name, readings in list(temps.items())[:2]:
            for r in readings[:2]:
                results.append(f"{name}: {r.current:.0f}°C")
        return "Temperatures: " + ", ".join(results) + ", sir."
    except ImportError:
        return "psutil not installed."
    except Exception as e:
        return f"Temperature unavailable: {e}"
