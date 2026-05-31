"""
jarvis/memory/conversation.py
In-memory conversation history manager.
Keeps a rolling window of user/assistant turns and can
export the full history for LLM context injection.
"""
from dataclasses import dataclass, field
from datetime import datetime
from jarvis.config import MAX_HISTORY_TURNS


@dataclass
class Turn:
    role:      str          # "user" or "assistant"
    content:   str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


class ConversationMemory:
    """
    Rolling conversation window.

    Usage:
        mem = ConversationMemory()
        mem.add("user", "What is Python?")
        mem.add("assistant", "Python is a high-level programming language...")
        history = mem.to_messages()   # pass to OllamaClient.chat()
    """

    def __init__(self, max_turns: int = MAX_HISTORY_TURNS):
        self.max_turns = max_turns
        self._turns: list[Turn] = []

    # ── write ─────────────────────────────────────────────────────────────────

    def add(self, role: str, content: str):
        """Append a new turn. Trims oldest if over max_turns."""
        self._turns.append(Turn(role=role, content=content))
        # Each "turn" = 1 user + 1 assistant message; keep 2*max_turns messages
        if len(self._turns) > self.max_turns * 2:
            self._turns = self._turns[-(self.max_turns * 2):]

    # ── read ──────────────────────────────────────────────────────────────────

    def to_messages(self) -> list[dict]:
        """Return history as OpenAI/Ollama-compatible message list."""
        return [{"role": t.role, "content": t.content} for t in self._turns]

    def last_n(self, n: int) -> list[Turn]:
        """Return the last n turns."""
        return self._turns[-n:]

    def last_user_message(self) -> str | None:
        for t in reversed(self._turns):
            if t.role == "user":
                return t.content
        return None

    # ── utility ───────────────────────────────────────────────────────────────

    def clear(self):
        """Wipe all history."""
        self._turns.clear()

    def summary(self) -> str:
        """One-line summary of the current history size."""
        return f"History: {len(self._turns)} messages ({len(self._turns)//2} turns)"

    def export_text(self) -> str:
        """Export full conversation as readable text."""
        lines = []
        for t in self._turns:
            prefix = "You" if t.role == "user" else "Jarvis"
            lines.append(f"[{t.timestamp}] {prefix}: {t.content}")
        return "\n".join(lines)

    def __len__(self):
        return len(self._turns)
