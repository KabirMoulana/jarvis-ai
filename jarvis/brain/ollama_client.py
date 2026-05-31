"""
jarvis/brain/ollama_client.py
Robust Ollama API client with:
  - streaming and non-streaming modes
  - automatic retry with exponential back-off
  - conversation history injection
  - model health-check
"""
import json
import time
import requests
from jarvis.config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT, SYSTEM_PROMPT


class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        self.host  = host.rstrip("/")
        self.model = model
        self._session = requests.Session()

    # ── public ────────────────────────────────────────────────────────────────

    def chat(self, prompt: str, history: list[dict] | None = None,
             stream: bool = False) -> str:
        """
        Send a prompt (with optional history) to Ollama.
        history format: [{"role": "user"|"assistant", "content": "..."}]
        """
        messages = self._build_messages(prompt, history)
        if stream:
            return self._stream(messages)
        return self._generate(messages)

    def is_available(self) -> bool:
        """Return True if Ollama is reachable."""
        try:
            r = self._session.get(f"{self.host}/api/tags", timeout=3)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        """Return list of locally available model names."""
        try:
            r = self._session.get(f"{self.host}/api/tags", timeout=5)
            data = r.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    # ── private ───────────────────────────────────────────────────────────────

    def _build_messages(self, prompt: str, history: list[dict] | None) -> list[dict]:
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            msgs.extend(history[-20:])  # keep last 20 turns max
        msgs.append({"role": "user", "content": prompt})
        return msgs

    def _generate(self, messages: list[dict], retries: int = 3) -> str:
        payload = {"model": self.model, "messages": messages, "stream": False}
        for attempt in range(retries):
            try:
                r = self._session.post(
                    f"{self.host}/api/chat",
                    json=payload,
                    timeout=OLLAMA_TIMEOUT,
                )
                r.raise_for_status()
                return r.json()["message"]["content"].strip()
            except (requests.RequestException, KeyError) as e:
                wait = 2 ** attempt
                print(f"[Ollama] Attempt {attempt+1} failed ({e}). Retrying in {wait}s...")
                time.sleep(wait)
        return "Sorry, I couldn't reach my brain right now. Please try again."

    def _stream(self, messages: list[dict]) -> str:
        payload = {"model": self.model, "messages": messages, "stream": True}
        collected = []
        try:
            with self._session.post(
                f"{self.host}/api/chat",
                json=payload,
                stream=True,
                timeout=OLLAMA_TIMEOUT,
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    print(token, end="", flush=True)
                    collected.append(token)
            print()  # newline after stream
        except Exception as e:
            print(f"\n[Ollama] Stream error: {e}")
        return "".join(collected)
