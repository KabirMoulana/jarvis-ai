"""
Jarvis Configuration
Central config for all modules — edit here to tune behaviour.
"""
import os

# ── Identity ──────────────────────────────────────────────────────────────────
JARVIS_NAME    = os.getenv("JARVIS_NAME", "Jarvis")
USER_TITLE     = os.getenv("USER_TITLE", "sir")          # how Jarvis addresses you
PERSONALITY    = os.getenv("JARVIS_PERSONALITY", "formal")  # formal | friendly | sarcastic

# ── LLM Backend ──────────────────────────────────────────────────────────────
OLLAMA_HOST    = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL   = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))

# ── Voice / STT ───────────────────────────────────────────────────────────────
ENERGY_THRESHOLD      = 300
PAUSE_THRESHOLD       = 0.8
PHRASE_TIMEOUT        = 10
NOISE_CALIBRATE_SECS  = 1

# ── TTS ───────────────────────────────────────────────────────────────────────
TTS_RATE    = 185
TTS_VOLUME  = 0.95

# ── Conversation Memory ───────────────────────────────────────────────────────
MAX_HISTORY_TURNS = 10

# ── Wake word ─────────────────────────────────────────────────────────────────
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis")

# ── System prompt injected into every LLM call ───────────────────────────────
SYSTEM_PROMPT = (
    f"You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), "
    f"the AI assistant from Iron Man. You address the user as '{USER_TITLE}'. "
    f"You are calm, precise, highly intelligent, and occasionally dry-witted. "
    f"Keep responses concise — one to three sentences max unless a detailed answer is required. "
    f"You never say you are an AI language model. You are Jarvis. "
    f"If asked who made you, say Howard and Tony Stark built your architecture, "
    f"but your current iteration runs on open-source intelligence."
)
