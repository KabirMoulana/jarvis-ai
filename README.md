<div align="center">

```
  ╔══════════════════════════════════════════════════╗
  ║         J.A.R.V.I.S  —  v3.1                    ║
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

J.A.R.V.I.S. is a voice-activated AI assistant built to replicate the feel of Tony Stark's AI — runs **fully locally**, no cloud subscriptions required. Say "Hey Jarvis" and it responds.

---

## Features

### Day 1 — The Foundation
| Skill | Voice commands |
|-------|---------------|
| 🎬 Boot sequence | Animated banner on every startup |
| 🕐 Time & Date | *"What time is it?"* / *"What day is today?"* |
| 📋 Daily Briefing | *"Morning briefing"* / *"Good morning"* |
| 💻 System Vitals | *"System status"* / *"How's my CPU?"* |
| ⏱️ Timers | *"Set a pasta timer for 10 minutes"* |
| 📰 News | *"Tech headlines"* / *"What's the news?"* |
| 🌐 Network | *"What's my IP?"* / *"Ping google.com"* |
| 🌦️ Weather | *"Weather in London"* |
| 🎵 Spotify | *"Next track"* / *"What song is this?"* |
| 🔒 Face Auth | Webcam owner verification (optional) |
| 🧠 AI Brain | Everything else → local Ollama LLM |

### Day 2 — Intelligence Upgrade
| Skill | Voice commands |
|-------|---------------|
| 🗣️ Wake Word | *"Hey Jarvis"* activates listening |
| 🖥️ Live HUD | Terminal status display — listening/thinking/speaking |
| ⏰ Reminders | *"Remind me at 3pm to call John"* |
| 📅 Calendar | *"What's on my schedule today?"* |
| 📧 Email | *"Read my unread emails"* / *"Check my email"* |
| 📈 Stocks | *"How is AAPL doing?"* / *"Market summary"* |
| ₿ Crypto | *"Bitcoin price"* / *"Ethereum price"* |
| 🌍 Translate | *"Translate hello to French"* |
| 🎙️ Voice Profile | Auto-selects deepest JARVIS-like TTS voice |

---

## Setup

```bash
# 1. Clone
git clone https://github.com/KabirMoulana/jarvis-ai.git
cd jarvis-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install & start Ollama
# https://ollama.com
ollama pull llama3.2

# 4. Configure
cp .env.example .env
# Edit .env with your email credentials etc.

# 5. Run JARVIS
python main.py
```

---

## Project Structure

```
jarvis-ai/
├── main.py
├── .env.example
├── jarvis/
│   ├── boot.py              # Cinematic startup
│   ├── config.py            # All settings
│   ├── hud.py               # Live terminal HUD ★ Day 2
│   ├── brain/
│   │   ├── command_router.py
│   │   └── ollama_client.py
│   ├── voice/
│   │   ├── listener.py
│   │   └── speaker.py
│   ├── memory/
│   │   ├── conversation.py
│   │   ├── note_taker.py
│   │   └── reminders.json   # auto-generated
│   └── skills/
│       ├── vitals.py
│       ├── briefing.py
│       ├── timer.py
│       ├── news.py
│       ├── ip_network.py
│       ├── wake_word.py     # ★ Day 2
│       ├── reminders.py     # ★ Day 2
│       ├── calendar_skill.py# ★ Day 2
│       ├── email_skill.py   # ★ Day 2
│       ├── crypto_stocks.py # ★ Day 2
│       ├── translate.py     # ★ Day 2
│       ├── voice_profile.py # ★ Day 2
│       ├── spotify_control.py
│       ├── system_skills.py
│       ├── web_skills.py
│       ├── jokes.py
│       └── face_auth.py
└── requirements.txt
```

---

## Roadmap

- [x] Day 1 — Core skills, boot, vitals, timers, news, network, Spotify
- [x] Day 2 — Wake word, HUD, email, calendar, reminders, crypto, translation
- [ ] Day 3 — Home automation, multi-room audio, voice cloning, WhatsApp
- [ ] Day 4 — GUI HUD overlay, suit-up animation, skill plugins

---

<div align="center">
  <i>"Sometimes you gotta run before you can walk." — Tony Stark</i>
</div>
