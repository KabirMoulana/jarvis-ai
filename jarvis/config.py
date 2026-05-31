"""
Jarvis Configuration
Central config for all modules — edit here to tune behaviour.
"""
import os

# ── LLM Backend ──────────────────────────────────────────────────────────────
OLLAMA_HOST   = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))

# ── Voice / STT ───────────────────────────────────────────────────────────────
ENERGY_THRESHOLD      = 300      # mic sensitivity
PAUSE_THRESHOLD       = 0.8      # seconds of silence = end of utterance
PHRASE_TIMEOUT        = 10       # max seconds to wait for speech
NOISE_CALIBRATE_SECS  = 1        # ambient noise calibration duration

# ── TTS ───────────────────────────────────────────────────────────────────────
TTS_RATE    = 185    # words-per-minute for pyttsx3
TTS_VOLUME  = 0.95

# ── Conversation Memory ───────────────────────────────────────────────────────
MAX_HISTORY_TURNS = 10   # how many past exchanges to keep in context

# ── Wake word ─────────────────────────────────────────────────────────────────
WAKE_WORD = "jarvis"

# ── System prompt injected into every LLM call ───────────────────────────────
SYSTEM_PROMPT = (
    "You are Jarvis, a highly intelligent AI assistant. "
    "Be concise, accurate, and helpful. "
    "When you don't know something, say so clearly."
)
