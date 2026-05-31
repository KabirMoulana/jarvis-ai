<div align="center">

```
  ╔══════════════════════════════════════════════════╗
  ║         J.A.R.V.I.S  —  v3.0                    ║
  ║   Just A Rather Very Intelligent System          ║
  ╚══════════════════════════════════════════════════╝
```

**An open-source Iron Man JARVIS — voice-powered, locally-run AI assistant**

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat-square)

</div>

---

## What is this?

J.A.R.V.I.S. is a voice-activated AI assistant built to replicate the feel of Tony Stark's AI — runs locally on your machine, no cloud subscriptions required. Speak to it, and it responds.

---

## Features (Day 1)

| Skill | Command examples |
|-------|-----------------|
| 🎬 Cinematic boot | Starts with an animated banner every time |
| 🕐 Time & Date | "What time is it?" / "What day is today?" |
| 📋 Daily Briefing | "Morning briefing" / "Good morning" |
| 💻 System Vitals | "System status" / "How's my CPU?" / "Check battery" |
| ⏱️ Timers | "Set a timer for 10 minutes" / "Set a pasta timer for 20 minutes" |
| 📰 News | "What's the news?" / "Tech headlines" |
| 🌐 Network | "What's my IP?" / "Ping google.com" / "Check internet" |
| 🌦️ Weather | "Weather in London" |
| 🎵 Spotify | "Play next track" / "What song is this?" / "Pause" |
| 🔍 Search | "Search for quantum computing" / "Wikipedia Einstein" |
| 📝 Notes | "Note that meeting at 3pm" / "Show my notes" |
| 😄 Jokes | "Tell me a joke" |
| 🧠 AI Brain | Everything else → Ollama LLM (llama3.2) |

---

## Setup

```bash
# 1. Clone
git clone https://github.com/KabirMoulana/jarvis-ai.git
cd jarvis-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install & start Ollama (local LLM)
# https://ollama.com
ollama pull llama3.2

# 4. Copy env config
cp .env.example .env

# 5. Run JARVIS
python main.py
```

### Environment Variables (`.env`)
```env
JARVIS_NAME=Jarvis
USER_TITLE=sir
OLLAMA_MODEL=llama3.2
WAKE_WORD=jarvis
```

---

## Project Structure

```
jarvis-ai/
├── main.py                    # Entry point
├── jarvis/
│   ├── boot.py                # Cinematic startup sequence
│   ├── config.py              # All settings
│   ├── brain/
│   │   ├── command_router.py  # Intent detection
│   │   └── ollama_client.py   # Local LLM interface
│   ├── voice/
│   │   ├── listener.py        # Microphone → text
│   │   └── speaker.py        # Text → speech
│   ├── memory/
│   │   ├── conversation.py    # Rolling conversation memory
│   │   └── note_taker.py     # Persistent notes
│   └── skills/
│       ├── vitals.py          # CPU, RAM, battery
│       ├── briefing.py        # Daily briefing
│       ├── timer.py           # Countdown timers
│       ├── news.py            # News headlines
│       ├── ip_network.py      # Network diagnostics
│       ├── spotify_control.py # Spotify control
│       ├── system_skills.py   # App launcher, volume
│       ├── web_skills.py      # Search, Wikipedia, weather
│       ├── jokes.py           # Jokes
│       └── face_auth.py       # Face recognition (optional)
└── requirements.txt
```

---

## Roadmap

- [x] Day 1 — Core skills, boot sequence, vitals, timers, news, network
- [ ] Day 2 — Wake word detection, email reading, calendar, reminders
- [ ] Day 3 — Home automation, multi-language, voice cloning
- [ ] Day 4 — GUI HUD display, suit-up animation

---

<div align="center">
  <i>"Sometimes you gotta run before you can walk." — Tony Stark</i>
</div>
