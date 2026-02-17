# 🎬 MediaAgentIQ

**AI Agent Platform for Media & Broadcast Operations**

8 specialized AI agents working 24/7 to automate your broadcast workflow - from captioning to compliance, viral clips to rights management.

![Dashboard Preview](https://img.shields.io/badge/Status-Demo%20Ready-green) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)

---

## 🤖 The 8 AI Agents

| Agent | Purpose | Value |
|-------|---------|-------|
| 🎬 **Clip Agent** | Monitors live broadcasts, identifies viral moments, auto-creates social clips | 10x more social content |
| 📝 **Caption Agent** | Auto-generates captions, QA checks, fixes timing issues | 80% cost reduction |
| ⚖️ **Compliance Agent** | Monitors 24/7 for FCC violations, profanity, political ad issues | Avoid $500K+ fines |
| 🔍 **Archive Agent** | Natural language search like "Find all Biden economy clips from Q3" | Instant archive access |
| 📱 **Social Publishing** | Creates Twitter/Instagram/TikTok posts, schedules posting | Always-on social presence |
| 🌍 **Localization Agent** | Auto-translates captions, generates dubs, multi-language workflows | Faster global distribution |
| 📜 **Rights Agent** | Tracks licenses, alerts before expiry, monitors unauthorized usage | Avoid legal disputes |
| 📈 **Trending Agent** | Monitors social media, news feeds, alerts newsroom to breaking stories | Never miss a story |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/MediaAgentIQ.git
cd MediaAgentIQ

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Windows Quick Start
Just double-click `run.bat`

### Access
Open your browser: **http://localhost:8000**

---

## 📸 Screenshots

### Dashboard
The main dashboard showing all 8 AI agents with real-time statistics and activity feed.

### Agent UIs
Each agent has a dedicated interface for uploading content, viewing results, and downloading outputs.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, FastAPI
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
- **Database:** SQLite (async with aiosqlite)
- **AI:** Mock responses (OpenAI integration ready)
- **Server:** Uvicorn ASGI

---

## 📁 Project Structure

```
MediaAgentIQ/
├── app.py                    # FastAPI application
├── config.py                 # Configuration
├── database.py               # SQLite setup
├── requirements.txt          # Dependencies
├── run.bat                   # Windows launcher
│
├── agents/                   # 8 AI Agent implementations
│   ├── caption_agent.py
│   ├── clip_agent.py
│   ├── archive_agent.py
│   ├── compliance_agent.py
│   ├── social_publishing_agent.py
│   ├── localization_agent.py
│   ├── rights_agent.py
│   └── trending_agent.py
│
├── templates/                # HTML templates (9 pages)
├── static/                   # CSS & JavaScript
├── uploads/                  # User uploads
└── outputs/                  # Generated files
```

---

## 📖 Documentation

See [MEDIAAGENTIQ_DOCUMENTATION.md](MEDIAAGENTIQ_DOCUMENTATION.md) for complete API reference, database schema, and deployment guide.

---

## 🔮 Roadmap

- [ ] Real OpenAI Whisper integration
- [ ] Video processing with FFmpeg
- [ ] User authentication
- [ ] Real-time WebSocket updates
- [ ] Email/Slack notifications
- [ ] Mobile companion app

---

## 📝 License

MIT License - feel free to use for your own projects!

---

**Built with ❤️ for Media & Broadcast professionals**
