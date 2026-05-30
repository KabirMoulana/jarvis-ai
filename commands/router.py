
"""Routes incoming commands to the appropriate handler."""
from commands import time_command, weather_command, web_search_command
from commands import system_command, notes_command
from utils.ollama_client import OllamaClient

_client = OllamaClient()
SYSTEM_PROMPT = (
    "You are Jarvis, an intelligent and concise AI assistant. "
    "Keep answers short and clear unless asked for detail."
)


def route(command: str) -> str:
    """Try each command handler; fall back to AI if none matches."""
    command = command.lower().strip()

    for handler in [
        time_command,
        weather_command,
        web_search_command,
        system_command,
        notes_command,
    ]:
        result = handler.handle(command)
        if result is not None:
            return result

    # Fallback to LLM
    return _client.generate(command, system=SYSTEM_PROMPT)
