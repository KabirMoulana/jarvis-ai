"""
jarvis/skills/plugin_manager.py
Plugin manager — allows JARVIS to load custom user skills
from a plugins directory at runtime.
Drop a .py file in ~/jarvis_plugins/ and JARVIS loads it automatically.
"""
import os
import importlib.util
import sys

_PLUGIN_DIR = os.path.expanduser("~/jarvis_plugins")
_loaded_plugins: dict = {}


def load_plugins() -> str:
    """Scan plugin directory and load all valid plugin files."""
    global _loaded_plugins
    os.makedirs(_PLUGIN_DIR, exist_ok=True)

    plugin_files = [f for f in os.listdir(_PLUGIN_DIR) if f.endswith(".py")]
    if not plugin_files:
        return "No plugins found in ~/jarvis_plugins, sir."

    loaded = []
    failed = []

    for filename in plugin_files:
        name = filename[:-3]
        path = os.path.join(_PLUGIN_DIR, filename)
        try:
            spec   = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _loaded_plugins[name] = module
            loaded.append(name)
        except Exception as e:
            failed.append(f"{name} ({e})")

    parts = []
    if loaded: parts.append(f"Loaded: {', '.join(loaded)}")
    if failed: parts.append(f"Failed: {', '.join(failed)}")
    return " | ".join(parts) + ", sir." if parts else "No plugins loaded, sir."


def list_plugins() -> str:
    """List all loaded plugins."""
    if not _loaded_plugins:
        return "No plugins loaded, sir. Drop .py files into ~/jarvis_plugins/"
    plugins = list(_loaded_plugins.keys())
    return f"Loaded plugins: {', '.join(plugins)}, sir."


def run_plugin(plugin_name: str, *args) -> str:
    """Run a function from a loaded plugin."""
    plugin = _loaded_plugins.get(plugin_name)
    if not plugin:
        return f"Plugin '{plugin_name}' not loaded, sir."
    if hasattr(plugin, "run"):
        try:
            result = plugin.run(*args)
            return str(result)
        except Exception as e:
            return f"Plugin '{plugin_name}' error: {e}, sir."
    return f"Plugin '{plugin_name}' has no 'run()' function, sir."


def unload_plugin(plugin_name: str) -> str:
    """Unload a plugin."""
    if plugin_name in _loaded_plugins:
        del _loaded_plugins[plugin_name]
        return f"Plugin '{plugin_name}' unloaded, sir."
    return f"Plugin '{plugin_name}' not found, sir."


def create_plugin_template(name: str) -> str:
    """Create a starter plugin file."""
    os.makedirs(_PLUGIN_DIR, exist_ok=True)
    path     = os.path.join(_PLUGIN_DIR, f"{name}.py")
    template = f'''"""
{name} — JARVIS custom plugin.
Drop this file in ~/jarvis_plugins/ to load it.
"""

PLUGIN_NAME    = "{name}"
PLUGIN_VERSION = "1.0"


def run(*args) -> str:
    """Main entry point for the plugin."""
    return "Hello from {name} plugin!"


def get_commands() -> list:
    """Return commands this plugin handles."""
    return ["{name}"]
'''
    with open(path, "w") as f:
        f.write(template)
    return f"Plugin template created at {path}, sir."
