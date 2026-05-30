
"""Simple in-memory conversation history for context-aware LLM responses."""
from collections import deque
from typing import List, Dict


class ConversationMemory:
    def __init__(self, max_turns: int = 10):
        self._history: deque[Dict[str, str]] = deque(maxlen=max_turns * 2)

    def add(self, role: str, content: str) -> None:
        self._history.append({"role": role, "content": content})

    def get_context(self) -> str:
        """Return history as a formatted string for LLM context."""
        lines = []
        for msg in self._history:
            prefix = "User" if msg["role"] == "user" else "Jarvis"
            lines.append(f"{prefix}: {msg['content']}")
        return "\n".join(lines)

    def clear(self) -> None:
        self._history.clear()
