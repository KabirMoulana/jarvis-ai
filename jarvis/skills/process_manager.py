"""
jarvis/skills/process_manager.py
Process manager — JARVIS lists, kills, and monitors running processes.
"""
import subprocess
import sys


def list_top_processes(count: int = 5) -> str:
    """List top CPU-consuming processes."""
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                procs.append(p.info)
            except Exception:
                pass
        procs.sort(key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)
        top   = procs[:count]
        parts = [f"{p['name']} (CPU: {p['cpu_percent']:.1f}%, RAM: {p['memory_percent']:.1f}%)"
                 for p in top if p.get("name")]
        return f"Top {len(parts)} processes, sir: " + "; ".join(parts) + "."
    except ImportError:
        return "psutil not installed. Run: pip install psutil"


def kill_process(name: str) -> str:
    """Kill a process by name."""
    try:
        import psutil
        killed = []
        for p in psutil.process_iter(["pid", "name"]):
            try:
                if name.lower() in p.info["name"].lower():
                    p.kill()
                    killed.append(p.info["name"])
            except Exception:
                pass
        if killed:
            return f"Terminated {', '.join(set(killed))}, sir."
        return f"No process named '{name}' found, sir."
    except ImportError:
        return "psutil not installed. Run: pip install psutil"


def get_memory_hogs(count: int = 5) -> str:
    """List processes using the most RAM."""
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(["pid", "name", "memory_percent"]):
            try:
                if p.info["memory_percent"]:
                    procs.append(p.info)
            except Exception:
                pass
        procs.sort(key=lambda x: x.get("memory_percent", 0), reverse=True)
        top   = procs[:count]
        parts = [f"{p['name']} ({p['memory_percent']:.1f}%)" for p in top]
        return f"Memory hogs, sir: " + ", ".join(parts) + "."
    except ImportError:
        return "psutil not installed."


def is_process_running(name: str) -> str:
    """Check if a specific process is running."""
    try:
        import psutil
        for p in psutil.process_iter(["name"]):
            try:
                if name.lower() in p.info["name"].lower():
                    return f"Yes, {p.info['name']} is currently running, sir."
            except Exception:
                pass
        return f"{name} is not running, sir."
    except ImportError:
        return "psutil not installed."


def get_open_ports() -> str:
    """List open network ports."""
    try:
        import psutil
        conns = psutil.net_connections(kind="inet")
        ports = sorted(set(c.laddr.port for c in conns if c.laddr and c.status == "LISTEN"))[:10]
        if not ports:
            return "No open listening ports detected, sir."
        return f"Open ports: {', '.join(map(str, ports))}, sir."
    except ImportError:
        return "psutil not installed."
    except Exception as e:
        return f"Port scan error: {e}"
