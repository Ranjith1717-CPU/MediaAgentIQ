# 🎬 MediaAgentIQ

**AI Agent Platform for Media & Broadcast Operations**

14 specialized AI agents working **autonomously 24/7** to automate your broadcast workflow — from captioning to compliance, deepfake detection to carbon intelligence.

![Version](https://img.shields.io/badge/Version-3.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.9+-green) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Agents](https://img.shields.io/badge/Agents-14-purple)

---

## ✨ What's New in v3.0 — Future-Ready Edition

- **🔮 6 New Future-Ready Agents** - Market gap innovations not yet available in broadcast
- **🕵️ Deepfake Detection** - 3-layer forensic AI synthetic media detection for live broadcasts
- **✅ Live Fact-Check** - Real-time claim verification across 8 fact databases during air
- **📊 Audience Intelligence** - Second-by-second viewer retention prediction & drop-off prevention
- **🎬 AI Production Director** - Autonomous camera cuts, lower-thirds, rundown optimization
- **🛡️ Brand Safety** - GARM-standard real-time contextual ad safety scoring
- **🌿 Carbon Intelligence** - Broadcast carbon footprint tracking & ESG report generation

---

## 🤖 The 14 AI Agents

### Original 8 (Market-Available)

| Agent | Purpose | Autonomous | Value |
|-------|---------|------------|-------|
| 🎬 **Clip Agent** | Detects viral moments using GPT-4 Vision | ✅ | 10x social content |
| 📝 **Caption Agent** | Transcribes with Whisper AI + QA checks | ✅ | 80% cost reduction |
| ⚖️ **Compliance Agent** | 24/7 FCC monitoring with AI analysis | ✅ Every 10min | Avoid $500K+ fines |
| 🔍 **Archive Agent** | Natural language search + MAM integration | ✅ | Instant access |
| 📱 **Social Publishing** | AI-generated posts for 5 platforms | ✅ | 24/7 presence |
| 🌍 **Localization** | Translation + ElevenLabs voice dubbing | ✅ | Global reach |
| 📜 **Rights Agent** | License tracking + violation detection | ✅ Every 1hr | Legal protection |
| 📈 **Trending Agent** | Real-time trend monitoring + alerts | ✅ Every 5min | Never miss a story |

### Future-Ready 6 (Market Gaps — Not Yet Available in Broadcast)

| Agent | Market Gap Addressed | Auto-Trigger | Key Standard |
|-------|---------------------|--------------|--------------|
| 🕵️ **Deepfake Detection** | AI synthetic media grew 900% in 2025 | On every upload | C2PA Provenance |
| ✅ **Live Fact-Check** | No real-time verification during live air | On caption complete | AP/Reuters/PolitiFact |
| 📊 **Audience Intelligence** | No second-by-second retention prediction | Every 5 min | Proprietary AI model |
| 🎬 **AI Production Director** | No autonomous broadcast production AI | Every 1 min | Human-approval gate |
| 🛡️ **Brand Safety** | No real-time contextual ad scoring | On every upload | GARM Standard |
| 🌿 **Carbon Intelligence** | No broadcast carbon tracking exists | Every 30 min | GHG Protocol / GRI 305 |

---

## 🚀 Quick Start

### Option 1: Streamlit Demo (Recommended)
```bash
cd MediaAgentIQ
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open: **http://localhost:8501**

### Option 2: FastAPI Backend
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
Open: **http://localhost:8000**

### Option 3: Autonomous Mode
```bash
python orchestrator.py
```
Agents run in background automatically!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MediaAgentIQ v3.0 Platform                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Original 8 Agents                                                           │
│  ┌────────┐ ┌──────┐ ┌──────────┐ ┌─────────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│  │Caption │ │ Clip │ │Compliance│ │ Archive │ │Social│ │Local │ │Rights│  │
│  └────────┘ └──────┘ └──────────┘ └─────────┘ └──────┘ └──────┘ └──────┘  │
│                                                                              │
│  Future-Ready 6 Agents (Market Gaps)                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │Deepfake  │ │  Live    │ │ Audience │ │  AI Prod │ │  Brand   │          │
│  │Detection │ │FactCheck │ │Intelligence│ │ Director │ │  Safety  │ Carbon  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│                              │                                               │
│            ┌─────────────────┴───────────────────┐                          │
│            │      Autonomous Orchestrator          │                          │
│            │  Task Queue • Scheduler • Events     │                          │
│            └─────────────────────────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  Services: Whisper AI • GPT-4 Vision • ElevenLabs Dubbing                   │
│  Integrations: Avid MAM • NMOS IS-04/05 • AWS/Azure • Social APIs           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
MediaAgentIQ/
├── streamlit_app.py               # 🖥️  Main Streamlit UI (14 agent pages)
├── orchestrator.py                # 🤖 Autonomous Agent Orchestrator
├── app.py                         # 🌐 FastAPI Backend
├── settings.py                    # ⚙️  Pydantic Configuration
│
├── agents/                        # 🤖 14 AI Agents
│   ├── base_agent.py             #    Dual-mode base class
│   │
│   │   — Original 8 —
│   ├── caption_agent.py          #    Whisper transcription
│   ├── clip_agent.py             #    GPT-4 Vision viral detection
│   ├── compliance_agent.py       #    FCC monitoring
│   ├── archive_agent.py          #    MAM integration
│   ├── social_publishing_agent.py
│   ├── localization_agent.py     #    ElevenLabs dubbing
│   ├── rights_agent.py
│   ├── trending_agent.py
│   │
│   │   — Future-Ready 6 —
│   ├── deepfake_detection_agent.py    # C2PA forensic analysis
│   ├── live_fact_check_agent.py       # 8-database real-time verification
│   ├── audience_intelligence_agent.py # Retention curve prediction
│   ├── ai_production_director_agent.py# Autonomous broadcast production
│   ├── brand_safety_agent.py          # GARM-standard ad scoring
│   └── carbon_intelligence_agent.py   # GHG Protocol ESG reporting
│
├── services/                      # 🔧 AI Service Wrappers
├── integrations/                  # 🔌 Avid MAM, NMOS IS-04/05
├── templates/                     # 📄 FastAPI HTML templates
├── static/                        # 🎨 CSS & JavaScript
└── .env.example                   # 🔑 API keys template
```

---

## ⚙️ Configuration

Create `.env` file:
```bash
# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# Mode
PRODUCTION_MODE=false  # true for real AI, false for demo

# Integrations (optional)
AVID_API_URL=https://your-avid-server/api
NMOS_REGISTRY_URL=http://nmos-registry:8080
```

---

## 🔌 Integrations

| System | Protocol | Status |
|--------|----------|--------|
| Media Asset Management | REST API, MOS, BXF | ✅ Ready |
| Broadcast Automation | MOS, VDCP, RS-422 | ✅ Ready |
| NMOS IP Infrastructure | IS-04, IS-05, IS-07 | ✅ Ready |
| Cloud Platforms | AWS, Azure, GCP | ✅ Ready |
| Social Media | Platform APIs, OAuth 2.0 | ✅ Ready |
| AI Transcription | Whisper, gRPC | ✅ Ready |
| Deepfake / C2PA Provenance | C2PA REST API | 🔮 Future Ready |
| Fact-Check Databases | REST API, RSS/Atom | 🔮 Future Ready |
| Audience Analytics | REST API, WebSocket | 🔮 Future Ready |
| Graphics & Newsroom (Vizrt, iNews) | Vizrt DataHub, MOS | 🔮 Future Ready |
| Brand Safety / Ad Tech | OpenRTB, IAS API | 🔮 Future Ready |
| Carbon ESG APIs (ElectricityMap) | REST API | 🔮 Future Ready |

---

## 🤖 Autonomous Mode

Agents run automatically in the background:

| Agent | Schedule | Trigger Events |
|-------|----------|----------------|
| Trending | Every 5 min | Breaking news alerts |
| Compliance | Every 10 min | Violation detection |
| Rights | Every 1 hour | Expiring licenses |
| Archive | Every 6 hours | Index optimization |
| Deepfake Detection | Every 2 min | Auto-hold suspicious content |
| Live Fact-Check | Every 3 min | Anchor alerts on false claims |
| Audience Intelligence | Every 5 min | Drop-off prevention cues |
| AI Production Director | Every 1 min | Camera + graphics decisions |
| Brand Safety | Every 2 min | Block unsafe ad insertions |
| Carbon Intelligence | Every 30 min | ESG metric updates |

**Event-Driven Chains:**
```
New Content  → Caption + Clip + Compliance + Archive + Deepfake + Brand Safety + Audience
Captions Done → Localization + Social + Live Fact-Check
Viral Clip   → Social Publishing
Breaking News → AI Production Director + Live Fact-Check
```

Start autonomous mode:
```bash
python orchestrator.py
```

---

## 📸 Features

### All-in-One Workflow
Process content through ALL 14 agents with one click:
- Upload once, analyze everywhere
- Real-time parallel processing across all 14 agents
- Combined results dashboard with 14-tab results view
- Batch export options

### Integration Showcase
- Live connection testing
- Architecture diagrams
- API documentation
- WebSocket & Webhook support

### Real-time Processing
- Step-by-step progress indicators
- Agent capability showcases
- Interactive demo workflows

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit, HTML5, Tailwind CSS |
| **Backend** | FastAPI, Python 3.9+ |
| **AI** | OpenAI (Whisper, GPT-4), ElevenLabs |
| **Database** | SQLite (async) |
| **Orchestration** | AsyncIO, Custom Scheduler |

---

## 📖 Documentation

- [Full Documentation](MEDIAAGENTIQ_DOCUMENTATION.md)
- API Reference: `http://localhost:8000/docs`

---

## ⚙️ Future-Ready Agent Configuration

Add to your `.env` file to tune the new agents:

```bash
# Deepfake Detection
DEEPFAKE_RISK_THRESHOLD=0.60      # 0.0-1.0, above this = hold from broadcast
DEEPFAKE_AUTO_HOLD=true
DEEPFAKE_SENSITIVITY=balanced     # strict | balanced | lenient

# Live Fact-Check
FACT_CHECK_AUTO_ALERT=true
FACT_CHECK_CLAIM_MIN_CONFIDENCE=0.70
FACT_CHECK_DATABASES=ap,reuters,politifact,factcheck_org,snopes

# Audience Intelligence
AUDIENCE_PREDICTION_INTERVAL_SECS=300
AUDIENCE_DROP_OFF_ALERT_THRESHOLD=0.04   # 4% drop triggers alert

# AI Production Director
PRODUCTION_DIRECTOR_AUTO_ACCEPT=false    # false = human approval required
PRODUCTION_DIRECTOR_CAMERA_LATENCY_MS=500

# Brand Safety
BRAND_SAFETY_DEFAULT_FLOOR=70     # 0-100 min score for ad insertion
BRAND_SAFETY_AUTO_BLOCK=true
BRAND_SAFETY_GARM_ENABLED=true

# Carbon Intelligence
CARBON_GRID_REGION=US_Northeast
CARBON_ESG_REPORT_ENABLED=true
CARBON_RENEWABLE_PPA=0.0          # % of electricity from renewable PPAs
```

---

## 🔮 Roadmap

- [x] Dual-mode architecture (demo + production)
- [x] Autonomous agent orchestrator
- [x] All-in-One workflow
- [x] Integration showcase
- [x] Real-time processing indicators
- [x] Deepfake detection agent
- [x] Live fact-check agent
- [x] Audience intelligence agent
- [x] AI production director agent
- [x] Brand safety agent (GARM)
- [x] Carbon intelligence agent (GHG Protocol)
- [ ] WebSocket real-time updates
- [ ] User authentication
- [ ] Mobile companion app
- [ ] Kubernetes deployment

---

## 📝 License

MIT License - Built for Media & Broadcast professionals

---

**MediaAgentIQ v3.0.0** | AI-Powered Media Operations Platform — Future-Ready Edition
