
# 🤖 Jarvis AI

An AI-powered voice assistant inspired by Tony Stark's JARVIS, built with Python.

## Features

- 🎤 Voice command recognition (Google Speech API)
- 🧠 AI responses via local Ollama LLM (llama3.2)
- 🕐 Time & date queries
- 🌤️ Weather lookup (no API key needed)
- 🔍 Web search via browser
- 📝 Note-taking
- 🖥️ System commands (open apps, shutdown, sleep)

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with `llama3.2` pulled
- Microphone

## Setup

```bash
git clone https://github.com/KabirMoulana/jarvis-ai.git
cd jarvis-ai
pip install -r requirements.txt
cp .env.example .env
python jarvis.py
```

## Configuration

Edit `.env` to change the Ollama host, model, or assistant name.

## Commands

| Say...                        | Action               |
|-------------------------------|----------------------|
| "What time is it?"            | Reports current time |
| "What's the weather in London" | Weather lookup       |
| "Search for Python tutorials" | Opens Google search  |
| "Take a note buy groceries"   | Saves a note         |
| "Read my notes"               | Reads saved notes    |
| "Open Safari"                 | Opens an app         |
| "Exit"                        | Shuts down Jarvis    |
