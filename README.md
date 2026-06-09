<div align="center">

```
  ╔══════════════════════════════════════════════════╗
  ║         J.A.R.V.I.S  —  v8.0  FINAL             ║
  ║   Just A Rather Very Intelligent System          ║
  ╚══════════════════════════════════════════════════╝
```

**An open-source Iron Man JARVIS — voice-powered, locally-run AI assistant**

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![Skills](https://img.shields.io/badge/Skills-185+-green?style=flat-square)
![Commits](https://img.shields.io/badge/Commits-259+-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-gold?style=flat-square)

</div>

---

## What is this?

J.A.R.V.I.S. is a voice-activated AI assistant that replicates Tony Stark's AI. Runs **fully locally**, responds to *"Hey Jarvis"*, and ships with **185+ skills** across 25 categories — built over 8 days of intensive development.

---

## Quick Start

```bash
git clone https://github.com/KabirMoulana/jarvis-ai.git
cd jarvis-ai
pip install -r requirements.txt
ollama pull llama3.2          # https://ollama.com
cp .env.example .env          # configure your keys
python main.py
```

---

## 185+ Skills Across 25 Categories

| Category | Skills |
|----------|--------|
| 🎬 **Core** | Boot sequence, wake word, HUD, voice profile, Iron Man persona, plugin system, JARVIS stats |
| 📋 **Productivity** | Reminders, alarms, timers, calendar, to-do, daily planner, focus mode, Pomodoro, time tracker, goal tracker, productivity report, task prioritizer |
| 💻 **System** | CPU/RAM/disk vitals, process manager, health monitor, screenshots, clipboard history, brightness, dark mode, system backup |
| 📧 **Communication** | Email reader, composer, scheduler, templates, WhatsApp messaging, contact book |
| 📰 **Information** | News headlines, news summarizer, weather alerts, tech news (HN/TC/dev.to), Wikipedia deep, science facts, quick facts, language facts |
| 💰 **Finance** | Crypto prices/alerts/portfolio, stock screener, forex rates, budget planner, investment calculator, financial concepts |
| 🎵 **Media** | Spotify control, music mood, internet radio, ambient sounds, music theory, music info, podcast finder |
| 🌍 **World** | World clock, IP geolocation, weather, air quality, traffic, travel planner, satellite tracker, solar system, world records |
| 🏋️ **Health** | Health tracker, workout tracker, sleep tracker, diet tracker, health alerts, meditation, food nutrition, mental health, reading tracker |
| 🧠 **Learning** | Flashcards, language quiz, geography quiz, trivia, brain games, vocabulary builder, interview prep, coding challenges, 30-day challenges |
| 🔧 **Developer** | API tester, regex helper, git helper, code runner, code explainer, number converter, acronym expander, periodic table, prompt library |
| 🌐 **Web** | Web search, Wikipedia, text summarizer, image search, AI image generation, startup news |
| 🏠 **Smart Home** | Home Assistant integration, device control, scenes (Movie/Sleep/Work/Party/Morning/Away), automation scheduler |
| 🎮 **Fun** | Jokes, trivia, brain games, word games, chess helper, story generator, magic 8-ball, morse code, idea generator |
| 📁 **Files** | File manager, file organizer, document reader, voice memos, clipboard history, PDF tools |
| 🔒 **Security** | Face authentication, password generator, 2FA TOTP, password vault (encrypted), network scanner |
| 🚀 **Space** | Astronomy, moon phase, ISS tracker, satellite passes, NASA APOD, solar system explorer |
| 🎉 **Events** | Event planner (birthday/wedding/conference), countdown tracker, birthday tracker, relationship tracker |
| 🛒 **Lifestyle** | Shopping list, recipe finder, home recipes, meal planner, book tracker, movie finder, travel planner |
| 💡 **Wisdom** | Life tips, quotes, daily challenge, debate helper, speech coach, psychology facts, art history |
| 🌱 **Environment** | Carbon footprint calculator (flights, commute, diet), reduction tips |
| 📊 **Analytics** | Session logger, sentiment analysis, productivity report, weekly streaks |
| 🎓 **Education** | Music theory, science facts, geography, language facts, art history, psychology |
| 🍳 **Kitchen** | Cooking timer (pasta/steak/eggs), ingredient-based recipes, meal suggestions |
| 🧩 **Extras** | Mind map generator, number base converter, solar system explorer, world records |

---

## Architecture

```
jarvis-ai/
├── main.py                 # Entry point — boots JARVIS
├── jarvis/
│   ├── boot.py             # Cinematic startup sequence
│   ├── config.py           # Central configuration
│   ├── hud.py              # Terminal HUD display
│   ├── brain/
│   │   ├── command_router.py   # Intent detection
│   │   └── ollama_client.py    # Local LLM interface
│   ├── voice/
│   │   ├── listener.py     # Microphone → text (STT)
│   │   └── speaker.py      # Text → speech (TTS)
│   ├── memory/
│   │   ├── conversation.py # Rolling chat history
│   │   ├── note_taker.py   # Persistent notes
│   │   └── session_log.py  # Interaction logging
│   └── skills/             # 185+ skill modules
└── requirements.txt
```

---

## Development Timeline

| Day | Commits | Highlights |
|-----|---------|-----------|
| Day 1 | 13 | Boot, vitals, timers, news, Spotify |
| Day 2 | 13 | Wake word, HUD, email, calendar, crypto |
| Day 3 | 21 | Smart home, alarms, health, focus |
| Day 4 | 30 | GUI HUD, WhatsApp, object detection |
| Day 5 | 50 | Portfolio, travel, games, radio, 35 more |
| Day 6 | 28 | Budget, interview prep, PDF tools, digest |
| Day 7 | 15 | Ideas, carbon, vault, meal planner, challenges |
| Day 8 | 20 | Chess, recipes, world records, psychology, music theory |
| **Total** | **190+** | **185+ skills, 259+ commits** |

---

<div align="center">

**Built by [KabirMoulana](https://github.com/KabirMoulana)**

*"Sometimes you gotta run before you can walk." — Tony Stark*

⭐ Star this repo if JARVIS impressed you

</div>
