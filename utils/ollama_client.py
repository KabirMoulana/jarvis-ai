
"""Ollama API client with optional conversation memory."""
import requests
import os
from typing import Optional
from utils.memory import ConversationMemory


class OllamaClient:
    def __init__(self, host: Optional[str] = None, model: Optional[str] = None):
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        self.memory = ConversationMemory()

    def generate(self, prompt: str, system: str = "") -> str:
        context = self.memory.get_context()
        full_prompt = f"{context}\nUser: {prompt}\nJarvis:" if context else prompt
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system
        try:
            resp = requests.post(f"{self.host}/api/generate", json=payload, timeout=30)
            resp.raise_for_status()
            answer = resp.json().get("response", "").strip()
            self.memory.add("user", prompt)
            self.memory.add("assistant", answer)
            return answer
        except requests.exceptions.ConnectionError:
            return "Sorry, I cannot reach the AI model. Is Ollama running?"
        except requests.exceptions.Timeout:
            return "The AI model took too long to respond."
        except Exception as e:
            return f"AI error: {e}"

    def is_available(self) -> bool:
        try:
            requests.get(f"{self.host}/api/tags", timeout=3)
            return True
        except Exception:
            return False

    def clear_memory(self) -> None:
        self.memory.clear()
