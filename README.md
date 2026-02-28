# 🎬 MediaAgentIQ

**AI Agent Platform for Media & Broadcast Operations**

19 specialized AI agents running **autonomously 24/7** across the full broadcast pipeline — from ingest to playout, captioning to compliance, deepfake detection to carbon intelligence. Agents are now reachable directly from **Slack and Microsoft Teams**.

![Version](https://img.shields.io/badge/Version-3.3.0-blue) ![Python](https://img.shields.io/badge/Python-3.9+-green) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Agents](https://img.shields.io/badge/Agents-19-purple) ![Channels](https://img.shields.io/badge/Channels-Slack%20%7C%20Teams-orange) ![Memory](https://img.shields.io/badge/Memory-Persistent%20.md%20Logs-teal) ![HOPE](https://img.shields.io/badge/HOPE-Standing%20Instructions-red)

---

## ✨ What's New in v3.3 — HOPE Engine Edition

- **🔮 HOPE Engine** — Standing-instruction layer. Tell an agent something once from Slack and it acts autonomously every time, forever, until you cancel: _"Whenever you detect breaking war news, alert me immediately"_
- **📋 Per-Agent Companion Files** — OpenClaw-style `HOPE.md`, `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md` auto-created per agent in `memory/agents/{slug}/`
- **🔇 Mute Hours + Rate Limiting** — Quiet hours (23:00–07:00) suppress non-CRITICAL alerts. 10 alerts/hour cap for NORMAL/HIGH. CRITICAL always fires
- **📬 4th Gateway Routing Tier** — HOPE intent detection intercepts standing-instruction phrases (`whenever`, `alert me if`, `watch for`, `stop watching`, `list my rules`) before LLM fallback
- **👤 UserProfile** — `memory/system/USER.md` maps alert priority to Slack channels (DM / #breaking-alerts / #media-alerts / digest)
- **4 new HOPE_* settings** — `HOPE_ENABLED`, `HOPE_MAX_ALERTS_PER_HOUR`, `HOPE_MUTE_START_HOUR`, `HOPE_MUTE_END_HOUR`
- **3 new slash commands** — `/miq-hope`, `/miq-hope-cancel`, `/miq-hope-list`

---

## ✨ What's New in v3.2 — Persistent Agent Memory Edition

- **🧠 Persistent Agent Memory** — Every agent now accumulates knowledge across runs. Per-agent `.md` log files track decisions, durations, inputs, outputs, and triggered events
- **📋 Inter-Agent Event Log** — `inter_agent_comms.md` captures every cross-agent event with source, subscribers, and payload summaries
- **📜 Global Task History** — `task_history.md` maintains a compact audit trail of every task across all 19 agents
- **🗂️ System State Snapshots** — `system_state.md` is fully rewritten every 5 minutes with queue size, agent registry, job schedules, and recent task history
- **🤖 LLM Context Injection** — `agent.get_memory_context_prompt()` surfaces the last N entries as a formatted system-prompt block for context-aware decisions
- **🔧 8 new MEMORY_* settings** — Fully configurable: max entries per file, trim thresholds, context window size, snapshot interval, all on by default with zero API key requirements

---

## ✨ What Was New in v3.1 — Pipeline + Channel Edition

- **🔌 Connector Framework** — MCP-style plugin architecture. Connect any external system as a tool agents can discover and call
- **💬 Slack & Teams Integration** — Trigger any agent directly from Slack (`/miq-compliance`) or Teams. Get interactive results with action buttons
- **🧠 Conversational Gateway** — NLP + slash commands. Natural language routing via Claude LLM with multi-turn conversation context
- **📥 Ingest & Transcode Agent** — Front-door of the broadcast pipeline. FFmpeg / AWS MediaConvert with 6 output profiles
- **📡 Signal Quality Monitor Agent** — EBU R128 loudness, black frame, freeze detection, NOC alerts
- **📺 Playout & Scheduling Agent** — Automation server integration (Harmonic, GV Maestro), SCTE-35 break injection
- **🌐 OTT / Multi-Platform Distribution Agent** — HLS/DASH packaging, CDN publishing, adaptive bitrate
- **📰 Newsroom Integration Agent** — iNews/ENPS MOS sync, wire ingestion, rundown management

---

## 🤖 The 19 AI Agents

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

### Future-Ready 6 (Market Gaps)

| Agent | Market Gap Addressed | Auto-Trigger | Key Standard |
|-------|---------------------|--------------|--------------|
| 🕵️ **Deepfake Detection** | AI synthetic media grew 900% in 2025 | On every upload | C2PA Provenance |
| ✅ **Live Fact-Check** | No real-time verification during live air | On caption complete | AP/Reuters/PolitiFact |
| 📊 **Audience Intelligence** | No second-by-second retention prediction | Every 5 min | Proprietary AI model |
| 🎬 **AI Production Director** | No autonomous broadcast production AI | Every 1 min | Human-approval gate |
| 🛡️ **Brand Safety** | No real-time contextual ad scoring | On every upload | GARM Standard |
| 🌿 **Carbon Intelligence** | No broadcast carbon tracking exists | Every 30 min | GHG Protocol / GRI 305 |

### Phase 1 Pipeline Agents (Broadcast Pipeline Gaps)

| Agent | Pipeline Stage | Schedule | Integration |
|-------|---------------|----------|-------------|
| 📥 **Ingest & Transcode** | Ingest | On upload | FFmpeg / AWS MediaConvert |
| 📡 **Signal Quality Monitor** | Production | Every 2 min | FFprobe / EBU R128 |
| 📺 **Playout & Scheduling** | Distribution | Every 5 min | Harmonic / GV Maestro |
| 🌐 **OTT Distribution** | Distribution | Every 10 min | HLS/DASH / CloudFront / Akamai |
| 📰 **Newsroom Integration** | Pre-production | Every 3 min | iNews / ENPS / MOS |

---

## 💬 Trigger Agents from Slack & Teams

Users interact with agents directly in their existing workspace tools.

**Slash commands (power users):**
```
/miq-compliance https://cdn.example.com/clip.mp4
/miq-trending --live --topic=elections
/miq-deepfake https://storage.example.com/video.mp4
/miq-ingest https://s3.example.com/raw_footage.mxf
/miq-signal rtmp://live-stream/channel1
/miq-status
/miq-connectors
/miq-help

# HOPE — Standing Instructions
/miq-hope                          # Create a standing rule (interactive)
/miq-hope-list                     # List all active rules
/miq-hope-cancel hope_001          # Cancel a rule by ID
```

**Natural language (everyone):**
```
@mediaagentiq check compliance on today's 6pm news
@mediaagentiq what's trending right now?
@mediaagentiq is this video a deepfake?
@mediaagentiq translate the clip to Spanish
@mediaagentiq sync the newsroom rundown

# HOPE — fire-and-forget standing instructions
@mediaagentiq whenever you detect Trump speaking, alert me immediately
@mediaagentiq every morning send me a digest of breaking war news
@mediaagentiq alert me if brand safety score drops below 70
@mediaagentiq stop watching hope_001
@mediaagentiq list my rules for archive agent
```

**Interactive results with action buttons:**
```
┌────────────────────────────────────────┐
│ ⚖️ Compliance Scan Result              │
│ Risk Score: 12/100  ✅                  │
│ Issues Found: 0                         │
│ [📄 Full Report] [🔔 Alert Team] [✅ Reviewed] │
└────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Streamlit Demo (Recommended)
```bash
cd MediaAgentIQ
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open: **http://localhost:8501**

### Option 2: FastAPI Backend (with Slack/Teams gateway)
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
Open: **http://localhost:8000**  |  API Docs: **http://localhost:8000/docs**

### Option 3: Autonomous Mode (19 agents running 24/7)
```bash
python orchestrator.py
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          MediaAgentIQ v3.2 Platform                          │
├──────────────────────────────────────────────────────────────────────────────┤
│  User Channels                                                                │
│  ┌─────────────┐  ┌─────────────────┐  ┌────────────────┐                   │
│  │  Slack Bot  │  │  MS Teams Bot   │  │  Streamlit UI  │  FastAPI           │
│  │  /miq-* cmds│  │  Adaptive Cards │  │  (19 agents)   │                   │
│  └──────┬──────┘  └────────┬────────┘  └────────────────┘                   │
│         └─────────────┬────┘                                                 │
│  ┌───────────────────▼─────────────────────────────────┐                    │
│  │           Conversational Gateway                     │                    │
│  │  Router (NLP+slash) • Formatter (BlockKit/Cards)     │                    │
│  │  Conversation Context • Webhook Handler              │                    │
│  └───────────────────┬─────────────────────────────────┘                    │
│                      │                                                       │
│  ┌───────────────────▼─────────────────────────────────┐                    │
│  │              Autonomous Orchestrator                  │                    │
│  │   Task Queue (Priority) • Scheduler • Event System   │                    │
│  │   Inter-Agent Event Log • System State Snapshots     │                    │
│  └───────────────────┬─────────────────────────────────┘                    │
│                      │                                                       │
│  ┌───────────────────▼─────────────────────────────────┐                    │
│  │                Agent Layer (19 Agents)               │                    │
│  │  Original 8 • Future-Ready 6 • Phase 1 Pipeline 5   │                    │
│  └───────────────────┬─────────────────────────────────┘                    │
│                      │                                                       │
│  ┌───────────────────▼─────────────────────────────────┐                    │
│  │     HOPE Engine — Standing Instructions (NEW v3.3)   │                    │
│  │  HopeRule + HopeEngine • HOPE.md per agent           │                    │
│  │  Mute hours • Rate limiting • Daily digest           │                    │
│  │  UserProfile (USER.md) • 4-tier gateway routing      │                    │
│  └───────────────────┬─────────────────────────────────┘                    │
│                      │                                                       │
│  ┌───────────────────▼─────────────────────────────────┐                    │
│  │     Persistent Agent Memory Layer (v3.2)             │                    │
│  │  memory/agents/{slug}/ (HOPE + 5 companion files)    │                    │
│  │  inter_agent_comms.md • task_history.md (global)     │                    │
│  │  system_state.md (5min) • logs/YYYY-MM-DD.md         │                    │
│  └───────────────────┬─────────────────────────────────┘                    │
│                      │                                                       │
│  ┌───────────────────▼─────────────────────────────────┐                    │
│  │          Connector Framework / MCP Layer             │                    │
│  │  ┌──────┐ ┌──────┐ ┌────────┐ ┌───────┐ ┌────────┐  │                    │
│  │  │Slack │ │Teams │ │  MAM   │ │Playout│ │  CDN   │  │                    │
│  │  │ Bot  │ │ Bot  │ │ (Avid) │ │Harmonic│ │Akamai │  │                    │
│  │  └──────┘ └──────┘ └────────┘ └───────┘ └────────┘  │                    │
│  │  ┌──────┐ ┌──────┐ ┌────────┐ ┌───────┐             │                    │
│  │  │  S3  │ │iNews │ │FFmpeg/ │ │AWS    │             │                    │
│  │  │      │ │ MOS  │ │MediaCvt│ │Elemental            │                    │
│  │  └──────┘ └──────┘ └────────┘ └───────┘             │                    │
│  └─────────────────────────────────────────────────────┘                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
MediaAgentIQ/
├── streamlit_app.py               # 🖥️  Main Streamlit UI
├── orchestrator.py                # 🤖 Autonomous Orchestrator (19 agents, 14 schedules)
├── app.py                         # 🌐 FastAPI Backend + Gateway mount
├── settings.py                    # ⚙️  Pydantic Configuration (all env vars)
│
├── memory/                        # 🧠 Persistent Memory + HOPE Engine
│   ├── __init__.py                #    Exports AgentMemoryLayer, HopeEngine, HopeRule, UserProfile
│   ├── agent_memory.py            #    AgentMemoryLayer (per-agent .md logs, trimming, LLM context)
│   ├── hope_engine.py             #    🔮 NEW v3.3 — HopeRule dataclass + HopeEngine class
│   ├── user_profile.py            #    🔮 NEW v3.3 — UserProfile reads USER.md
│   ├── system/                   ←    auto-created at runtime
│   │   ├── USER.md                #    User notification prefs (Slack handle, timezone, channels)
│   │   └── IDENTITY.md            #    Platform metadata
│   └── agents/                   ←    auto-created at runtime
│       ├── {slug}/                #    Per-agent subdirectory (NEW v3.3)
│       │   ├── HOPE.md            #    Standing rules for this agent
│       │   ├── AGENTS.md          #    Agent relationships
│       │   ├── MEMORY.md          #    Task summaries
│       │   ├── SOUL.md            #    Agent personality
│       │   ├── TOOLS.md           #    Available tools
│       │   ├── IDENTITY.md        #    Agent metadata
│       │   └── logs/              #    Daily log files (YYYY-MM-DD.md)
│       ├── inter_agent_comms.md   #    Cross-agent event log
│       ├── task_history.md        #    Global audit trail (markdown table)
│       └── system_state.md        #    Orchestrator snapshot (rewritten every 300s)
│
├── gateway/                       # 💬 Conversational Channel Gateway
│   ├── __init__.py
│   ├── router.py                 #    NLP + slash command → agent routing
│   ├── formatter.py              #    Agent output → Slack Block Kit / Teams Cards
│   ├── conversation.py           #    Per-user multi-turn context
│   └── webhook_handler.py        #    FastAPI routes (/slack/*, /teams/*)
│
├── connectors/                    # 🔌 NEW — MCP-Style Connector Framework
│   ├── __init__.py               #    setup_connectors() startup helper
│   ├── base_connector.py         #    BaseConnector abstract class
│   ├── registry.py               #    ConnectorRegistry + call_tool() MCP dispatch
│   └── channels/                 #    User-facing channel connectors
│       ├── slack.py              #    Slack Bot (Block Kit, alerts, slash cmds)
│       └── teams.py              #    Teams Bot (Adaptive Cards, proactive alerts)
│
├── agents/                        # 🤖 19 AI Agents
│   ├── base_agent.py             #    Dual-mode base class
│   │   — Original 8 —
│   ├── caption_agent.py
│   ├── clip_agent.py
│   ├── compliance_agent.py
│   ├── archive_agent.py
│   ├── social_publishing_agent.py
│   ├── localization_agent.py
│   ├── rights_agent.py
│   ├── trending_agent.py
│   │   — Future-Ready 6 —
│   ├── deepfake_detection_agent.py
│   ├── live_fact_check_agent.py
│   ├── audience_intelligence_agent.py
│   ├── ai_production_director_agent.py
│   ├── brand_safety_agent.py
│   ├── carbon_intelligence_agent.py
│   │   — Phase 1 Pipeline 5 (NEW) —
│   ├── ingest_transcode_agent.py      # FFmpeg / AWS MediaConvert
│   ├── signal_quality_agent.py        # EBU R128, black frame, freeze
│   ├── playout_scheduling_agent.py    # Harmonic / GV Maestro
│   ├── ott_distribution_agent.py      # HLS/DASH / CDN
│   └── newsroom_integration_agent.py  # iNews / ENPS / MOS
│
├── services/                      # 🔧 AI Service Wrappers
│   ├── transcription.py          #    Whisper API
│   ├── vision.py                 #    GPT-4 Vision
│   └── dubbing.py                #    ElevenLabs
│
├── integrations/                  # 🔌 Broadcast System Integrations
│   ├── avid/                     #    Avid Media Central
│   └── grass_valley/             #    NMOS IS-04/IS-05
│
└── .env.example                   # 🔑 Environment variables template
```

---

## ⚙️ Configuration

### Core `.env` settings

```bash
# Mode
PRODUCTION_MODE=false          # true = real AI APIs, false = demo mode

# Memory Layer (enabled by default — no API keys needed)
MEMORY_ENABLED=true                        # Set false to disable all .md logging
MEMORY_DIR=memory                          # Root dir for agent memory files
MEMORY_MAX_ENTRIES_PER_AGENT=500           # Trim trigger per-agent file
MEMORY_TRIM_TO=400                         # Entries kept after trim
MEMORY_RECENT_CONTEXT_ENTRIES=5            # Entries injected into LLM prompts
MEMORY_INTER_AGENT_MAX_ENTRIES=2000        # Max entries in inter_agent_comms.md
MEMORY_TASK_HISTORY_MAX_ENTRIES=5000       # Max rows in task_history.md
MEMORY_SYSTEM_STATE_INTERVAL_SECS=300      # system_state.md rewrite interval

# HOPE Engine (enabled by default — no API keys needed)
HOPE_ENABLED=true                          # Set false to disable standing-instruction engine
HOPE_MAX_ALERTS_PER_HOUR=10               # Rate-limit non-critical alerts per hour
HOPE_MUTE_START_HOUR=23                   # Start of quiet hours (local time, 24h)
HOPE_MUTE_END_HOUR=7                      # End of quiet hours (CRITICAL bypasses mute)

# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# Slack Bot (for /miq-* commands and agent alerts)
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_DEFAULT_CHANNEL=#mediaagentiq

# Microsoft Teams Bot
TEAMS_APP_ID=...
TEAMS_APP_PASSWORD=...
TEAMS_TENANT_ID=your-tenant-id

# Phase 1 Pipeline Agents
AUTOMATION_SERVER_URL=http://harmonic-server/api   # Playout
AUTOMATION_SERVER_TYPE=harmonic                     # harmonic | gv_maestro
CDN_PROVIDER=cloudfront                             # cloudfront | akamai | fastly
INEWS_API_URL=http://inews-server/api              # Newsroom

# Future-Ready Agent Settings
DEEPFAKE_RISK_THRESHOLD=0.60
PRODUCTION_DIRECTOR_AUTO_ACCEPT=false
BRAND_SAFETY_DEFAULT_FLOOR=70
CARBON_GRID_REGION=US_Northeast
```

---

## 🤖 Autonomous Mode — 14 Scheduled Jobs

| Agent | Schedule | Trigger Events |
|-------|----------|----------------|
| AI Production Director | Every 1 min | BREAKING_NEWS |
| Deepfake Detection | Every 2 min | NEW_CONTENT |
| Brand Safety | Every 2 min | NEW_CONTENT |
| Live Fact-Check | Every 3 min | CAPTION_COMPLETE, BREAKING_NEWS |
| Trending | Every 5 min | — |
| Audience Intelligence | Every 5 min | NEW_CONTENT |
| Playout & Scheduling | Every 5 min | — |
| Compliance | Every 10 min | — |
| OTT Distribution | Every 10 min | — |
| Newsroom Integration | Every 3 min | — |
| Signal Quality Monitor | Every 2 min | — |
| Rights | Every 1 hour | — |
| Carbon Intelligence | Every 30 min | — |
| Archive | Every 6 hours | — |

**Event-Driven Chains:**
```
New Content  → Caption + Clip + Compliance + Archive + Deepfake + Brand Safety + Audience + Ingest
Captions Done → Localization + Social + Live Fact-Check
Viral Clip   → Social Publishing
Breaking News → AI Production Director + Live Fact-Check
```

---

## 🔌 Connector Framework (MCP-Style)

The connector framework exposes external systems as tools that agents can discover and call — similar to MCP (Model Context Protocol).

```python
from connectors import connector_registry, setup_connectors

# Connect all channels at startup
await setup_connectors(demo_mode=True)

# Agent sends an alert via Slack
slack = connector_registry.get("slack")
await slack.send_alert("Signal Quality Critical", "Stream dropped", severity="critical")

# MCP-style tool call — agent doesn't need to know which connector handles it
result = await connector_registry.call_tool(
    "slack_send_message",
    {"channel": "#noc-alerts", "text": "Ingest job complete"}
)

# Discover all available tools (for LLM tool-use)
tools = connector_registry.get_all_tool_definitions()
```

**Available MCP Tools (v3.1):**
- `slack_send_message` — Send a Block Kit card to any Slack channel
- `slack_send_alert` — Send a severity-coded proactive alert
- `slack_read_channel` — Read recent messages from a channel
- `teams_send_message` — Send an Adaptive Card to Teams
- `teams_send_alert` — Send a proactive alert card to Teams

---

## 🌐 Slack Bot Setup

1. Create a Slack app at https://api.slack.com/apps
2. Enable **Event Subscriptions** → Request URL: `https://your-domain.com/slack/events`
3. Enable **Slash Commands** → add `/miq-*` commands pointing to `/slack/commands`
4. Enable **Interactivity** → Request URL: `https://your-domain.com/slack/actions`
5. Add Bot Token Scopes: `chat:write`, `channels:history`, `commands`
6. Install to workspace → copy Bot Token and Signing Secret to `.env`

## 🟦 Teams Bot Setup

1. Register a bot in Azure Bot Service
2. Set messaging endpoint: `https://your-domain.com/teams/messages`
3. Copy App ID and Password to `.env`
4. Add the bot to your Teams channel

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit, HTML5 |
| **Backend** | FastAPI, Python 3.9+ |
| **AI** | OpenAI (Whisper, GPT-4), ElevenLabs |
| **Channels** | Slack Bot SDK, Teams Bot Framework |
| **Transcoding** | FFmpeg, AWS MediaConvert |
| **Packaging** | AWS MediaPackage, HLS/DASH |
| **CDN** | Akamai, CloudFront, Fastly |
| **Newsroom** | iNews REST API, MOS Protocol |
| **Playout** | Harmonic Polaris, GV Maestro REST |
| **Database** | SQLite (async) |
| **Orchestration** | AsyncIO, Custom Scheduler |
| **Agent Memory** | Persistent `.md` logs, per-agent + global audit, LLM context injection |
| **HOPE Engine** | Standing-instruction `.md` rules, mute hours, rate limiting, daily digest |

---

## 📖 Documentation

- [Full Documentation](MEDIAAGENTIQ_DOCUMENTATION.md)
- API Reference: `http://localhost:8000/docs`
- Gateway Health: `http://localhost:8000/gateway/health`

---

## 📈 Changelog

### v3.3.0 (Latest) — HOPE Engine Edition
- ✅ `memory/hope_engine.py` — `HopeRule` dataclass + `HopeEngine` class (add/cancel/list/evaluate/fire)
- ✅ `memory/user_profile.py` — `UserProfile` reads `memory/system/USER.md` for Slack channel routing
- ✅ `memory/system/USER.md` + `IDENTITY.md` — OpenClaw-style platform identity + user preference files
- ✅ Per-agent `memory/agents/{slug}/` subdirs — `HOPE.md`, `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `logs/`
- ✅ `BaseAgent`: HOPE init + post-`process()` evaluation hook + `add/cancel/list_hope_rules()` methods
- ✅ 4th gateway routing tier — HOPE intent detection (9 trigger phrases) before LLM fallback
- ✅ `format_hope_created/cancelled/list/alert()` Slack Block Kit formatters (CRITICAL = `<!here>` + bold)
- ✅ Mute hours (23:00–07:00), CRITICAL bypasses mute; 10 alerts/hour rate limit per agent
- ✅ 3 new slash commands: `/miq-hope`, `/miq-hope-cancel`, `/miq-hope-list`
- ✅ 4 new `HOPE_*` settings in `settings.py`
- ✅ Failure-safe throughout: corrupt HOPE.md recreated from scratch; no exception propagates to agent

### v3.2.0 — Persistent Agent Memory Edition
- ✅ `memory/` Python package — `AgentMemoryLayer` class with per-agent `.md` log files
- ✅ Per-agent memory: entries/success rate/avg duration tracked in live header; auto-trim at configurable limits
- ✅ `inter_agent_comms.md` — cross-agent event log with source, subscribers, payload summary
- ✅ `task_history.md` — global compact audit trail (markdown table, max 5 000 rows)
- ✅ `system_state.md` — orchestrator snapshot fully rewritten every 300 s
- ✅ `BaseAgent.get_memory_context_prompt()` — inject last N entries into any LLM system prompt
- ✅ 8 new `MEMORY_*` settings in `settings.py` (all defaults work out-of-the-box)
- ✅ Failure-safe: all memory I/O wrapped in `try/except`; agents continue if `memory/` is absent
- ✅ Orchestrator `_handle_task_completion` now returns triggered-event list + logs to inter-agent comms

### v3.1.0 — Pipeline + Channel Edition
- ✅ Conversational Gateway — NLP + slash command routing to all 19 agents
- ✅ Slack Bot integration — Block Kit cards, slash commands, interactive buttons
- ✅ Microsoft Teams integration — Adaptive Cards, Bot Framework
- ✅ MCP-style Connector Framework — BaseConnector, ConnectorRegistry, tool discovery
- ✅ IngestTranscodeAgent — FFmpeg / AWS MediaConvert, 6 output profiles
- ✅ SignalQualityAgent — EBU R128 / ATSC A/85, black frame, freeze detection
- ✅ PlayoutSchedulingAgent — Harmonic / GV Maestro, SCTE-35 break injection
- ✅ OTTDistributionAgent — HLS/DASH, CloudFront/Akamai CDN, ABR ladder
- ✅ NewsroomIntegrationAgent — iNews/ENPS MOS sync, wire ingestion
- ✅ 4 new autonomous schedules (signal, newsroom, playout, OTT)
- ✅ Multi-turn conversation context across Slack/Teams sessions

### v3.0.0 — Future-Ready Edition
- ✅ 6 future-ready agents (Deepfake, Fact-Check, Audience, Production Director, Brand Safety, Carbon)
- ✅ Extended orchestrator with event subscriptions and scheduled jobs

### v2.0.0
- ✅ Autonomous Agent Orchestrator
- ✅ All-in-One Workflow
- ✅ MAM integration (Avid), NMOS integration (IS-04/IS-05)

### v1.0.0
- ✅ 8 AI agents (demo mode), FastAPI backend, basic Streamlit UI

---

## 🔮 Roadmap

- [x] Dual-mode architecture (demo + production)
- [x] Autonomous agent orchestrator (14 scheduled jobs)
- [x] 19 AI agents covering the broadcast pipeline
- [x] Slack Bot with slash commands + interactive cards
- [x] Microsoft Teams Bot with Adaptive Cards
- [x] MCP-style connector framework
- [x] Multi-turn conversational context
- [x] Persistent agent memory layer (.md logs per agent + global audit)
- [x] LLM context injection from agent memory
- [x] HOPE Engine — standing-instruction layer with autonomous Slack alerting
- [x] Per-agent OpenClaw-style companion files (HOPE.md, SOUL.md, IDENTITY.md, etc.)
- [ ] Pre-production agents (Story Intelligence, Script & Prompter, Rundown Planning)
- [ ] Technical QC Agent (full automated QC suite)
- [ ] Graphics Automation Agent (Vizrt / Chyron integration)
- [ ] Revenue Intelligence Agent
- [ ] NOC Monitoring Agent
- [ ] WebSocket real-time updates
- [ ] User authentication
- [ ] Kubernetes deployment

---

**MediaAgentIQ v3.3.0** | AI-Powered Broadcast Operations Platform — HOPE Engine Edition
