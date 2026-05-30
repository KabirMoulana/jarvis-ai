
"""Routes incoming commands to the appropriate handler."""
from commands import (
    time_command,
    weather_command,
    web_search_command,
    system_command,
    notes_command,
    reminder_command,
)
from utils.ollama_client import OllamaClient

_client = OllamaClient()
SYSTEM_PROMPT = (
    "You are Jarvis, an intelligent and concise AI assistant. "
    "Keep answers short and clear unless asked for detail."
)


def route(command: str) -> str:
    command = command.lower().strip()
    if command in ("exit", "quit", "bye", "shutdown jarvis"):
        return "exit"
    for handler in [
        time_command,
        weather_command,
        reminder_command,
        web_search_command,
        system_command,
        notes_command,
    ]:
        result = handler.handle(command)
        if result is not None:
            return result
    return _client.generate(command, system=SYSTEM_PROMPT)
