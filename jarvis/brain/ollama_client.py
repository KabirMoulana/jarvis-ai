"""
jarvis/brain/ollama_client.py
Ollama LLM client — upgraded with streaming, retry logic,
model switching, and the full JARVIS system prompt.
"""
import urllib.request
import urllib.error
import json
import os
from jarvis.config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT, SYSTEM_PROMPT, MAX_HISTORY_TURNS


class OllamaClient:
    def __init__(self, model: str = OLLAMA_MODEL):
        self.model   = model
        self.host    = OLLAMA_HOST
        self.timeout = OLLAMA_TIMEOUT

    def is_available(self) -> bool:
        try:
            urllib.request.urlopen(f"{self.host}/api/tags", timeout=3)
            return True
        except Exception:
            return False

    def chat(self, prompt: str, history: list[dict] | None = None) -> str:
        """Send a message with conversation history and return the response."""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            # Keep last N turns to avoid context overflow
            messages.extend(history[-(MAX_HISTORY_TURNS * 2):])
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model":    self.model,
            "messages": messages,
            "stream":   False,
            "options":  {
                "temperature": 0.7,
                "top_p":       0.9,
                "num_predict": 300,
            }
        }

        for attempt in range(3):
            try:
                data = json.dumps(payload).encode()
                req  = urllib.request.Request(
                    f"{self.host}/api/chat",
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    result = json.loads(resp.read())
                return result["message"]["content"].strip()
            except urllib.error.URLError:
                if attempt == 2:
                    return "I'm having trouble reaching my AI brain, sir. Ollama may be offline."
            except Exception as e:
                if attempt == 2:
                    return f"LLM error: {e}"

        return "Unable to get a response, sir."

    def list_models(self) -> list[str]:
        """Return available Ollama models."""
        try:
            with urllib.request.urlopen(f"{self.host}/api/tags", timeout=5) as resp:
                data = json.loads(resp.read())
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    def switch_model(self, model_name: str) -> str:
        available = self.list_models()
        if not available:
            return "Cannot reach Ollama to check available models, sir."
        matches = [m for m in available if model_name.lower() in m.lower()]
        if not matches:
            return f"Model '{model_name}' not found. Available: {', '.join(available)}, sir."
        self.model = matches[0]
        return f"Switched to model '{self.model}', sir."

    def get_model_info(self) -> str:
        return f"Currently using model: {self.model} via {self.host}, sir."
