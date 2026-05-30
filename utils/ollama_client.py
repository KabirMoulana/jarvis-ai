
"""Ollama API client for local LLM inference."""
import requests
import os
from typing import Optional


class OllamaClient:
    def __init__(self, host: Optional[str] = None, model: Optional[str] = None):
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")

    def generate(self, prompt: str, system: str = "") -> str:
        """Send a prompt to Ollama and return the response text."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system
        try:
            resp = requests.post(f"{self.host}/api/generate", json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return "Sorry, I cannot reach the AI model. Is Ollama running?"
        except requests.exceptions.Timeout:
            return "The AI model took too long to respond."
        except Exception as e:
            return f"AI error: {e}"

    def is_available(self) -> bool:
        """Check whether the Ollama server is reachable."""
        try:
            requests.get(f"{self.host}/api/tags", timeout=3)
            return True
        except Exception:
            return False
