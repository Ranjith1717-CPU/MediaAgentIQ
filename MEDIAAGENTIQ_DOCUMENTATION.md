# MediaAgentIQ v3.1 — Complete Documentation

## 📋 Overview

MediaAgentIQ is an enterprise AI-powered agent platform for media and broadcast organizations. It provides **19 specialized AI agents** that run **autonomously 24/7** across the full broadcast pipeline, and are now reachable directly from **Slack and Microsoft Teams**.

**Key Features:**
- 🤖 **Autonomous Operation** — 19 agents, 14 scheduled jobs, event-driven chains
- 🔄 **Dual-Mode Architecture** — Demo mode (no API keys) + Production mode (real AI)
- 💬 **Slack & Teams Integration** — Trigger any agent from your workspace via `/miq-*` slash commands or natural language
- 🔌 **MCP Connector Framework** — Plugin architecture. Any external system exposed as a tool agents can discover and call
- 🚀 **All-in-One Workflow** — Process content through all 19 agents simultaneously
- 🔮 **Future-Ready** — 6 market-gap agents solving problems no broadcast vendor has tackled

---

## 🚀 Quick Start

```bash
cd MediaAgentIQ
pip install -r requirements.txt

# Streamlit UI (recommended for demos)
streamlit run streamlit_app.py          # → http://localhost:8501

# FastAPI backend + Slack/Teams gateway
uvicorn app:app --reload                # → http://localhost:8000

# Autonomous background mode (all 19 agents)
python orchestrator.py
```

---

## 🏗️ Architecture

### System Layers

```
User Channels
  Slack Bot (/miq-* + @mentions + interactive cards)
  MS Teams Bot (Adaptive Cards + proactive alerts)
         │
Conversational Gateway    [gateway/]
  Router   → NLP intent + slash commands → agent selection
  Formatter → agent output → Slack Block Kit / Teams Adaptive Cards
  Context  → per-user multi-turn conversation state
  Webhooks → /slack/events, /slack/commands, /slack/actions, /teams/messages
         │
Autonomous Orchestrator   [orchestrator.py]
  Priority Task Queue (CRITICAL → HIGH → NORMAL → LOW)
  Scheduler (14 recurring jobs)
  Event System (8 event types, chain reactions)
         │
Agent Layer (19 agents)   [agents/]
  Original 8 + Future-Ready 6 + Phase 1 Pipeline 5
         │
Connector Framework       [connectors/]
  BaseConnector → ConnectorRegistry → MCP tool dispatch
  Channel: Slack, Teams
  System:  S3, Avid MAM, Harmonic, CloudFront, FFmpeg, iNews, ...
         │
Services Layer            [services/]
  Whisper AI (transcription)
  GPT-4 Vision (clip detection, deepfake, brand safety)
  ElevenLabs (voice dubbing)
```

### Dual-Mode Processing

Every agent supports two modes:
```python
class BaseAgent:
    async def process(self, input_data):
        await self.validate_input(input_data)
        if self.is_production_mode:
            return await self._production_process(input_data)  # Real AI/APIs
        else:
            return await self._demo_process(input_data)         # Realistic mock data
```

---

## 💬 Conversational Gateway

### How It Works

```
User in Slack: "/miq-compliance https://cdn.example.com/clip.mp4"
       ↓
Slack webhook → gateway/webhook_handler.py
       ↓
Gateway Router → slash command parser → agent_key="compliance", params={url:...}
       ↓
"Processing..." placeholder sent to Slack immediately
       ↓
ComplianceAgent.process({url: ...}) runs
       ↓
formatter.format_slack("compliance", result) → Block Kit JSON
       ↓
Slack chat.postMessage with interactive card + action buttons
       ↓
User clicks "📄 Full Report" → /slack/actions → action handler
```

### Routing Priority
1. **Slash command** (`/miq-*`) — deterministic, instant, no AI needed
2. **Keyword NLP** — regex pattern matching, ~85% confidence, no API call
3. **Claude LLM fallback** — for ambiguous or complex requests (requires `OPENAI_API_KEY`)

### Slash Commands Reference

| Command | Agent | Example |
|---------|-------|---------|
| `/miq-caption [url]` | Caption | `/miq-caption https://cdn.example.com/clip.mp4` |
| `/miq-compliance [url]` | Compliance | `/miq-compliance https://cdn.example.com/news.mp4` |
| `/miq-clip [url]` | Clip | `/miq-clip https://cdn.example.com/broadcast.mp4` |
| `/miq-trending [--live] [--topic=X]` | Trending | `/miq-trending --live --topic=elections` |
| `/miq-deepfake [url]` | Deepfake | `/miq-deepfake https://cdn.example.com/video.mp4` |
| `/miq-factcheck [text]` | Fact-Check | `/miq-factcheck "The minister said X"` |
| `/miq-social [url]` | Social | `/miq-social https://cdn.example.com/clip.mp4` |
| `/miq-archive [query]` | Archive | `/miq-archive election coverage 2024` |
| `/miq-brand [url]` | Brand Safety | `/miq-brand https://cdn.example.com/segment.mp4` |
| `/miq-ingest [url]` | Ingest | `/miq-ingest s3://bucket/raw.mxf` |
| `/miq-signal [stream]` | Signal Quality | `/miq-signal rtmp://live/channel1` |
| `/miq-playout` | Playout | `/miq-playout` |
| `/miq-ott [url]` | OTT | `/miq-ott s3://bucket/encoded.mp4` |
| `/miq-newsroom` | Newsroom | `/miq-newsroom --show="Evening News"` |
| `/miq-status` | System | `/miq-status` |
| `/miq-connectors` | Connectors | `/miq-connectors` |
| `/miq-help` | Help | `/miq-help` |

### Natural Language Examples

```
"Check compliance on the 6pm news segment"
"What's trending right now about the election?"
"Is this video a deepfake?" + [attach file URL]
"Translate the clip to Spanish and French"
"Generate social posts for the interview"
"Sync the newsroom rundown"
"What's the signal quality on stream 1?"
"Show me the playout schedule"
"Ingest the raw footage from S3"
```

### Multi-Turn Conversation

The gateway maintains conversation context per user per channel:
```
User:  "Check compliance on https://cdn.example.com/clip.mp4"
Bot:   [Compliance card — score 82/100]
User:  "Now generate social posts for it"       ← "it" resolved to same URL
Bot:   [Social Publishing card]
User:  "Translate those to Spanish"             ← context carries forward
Bot:   [Localization card]
```

---

## 🤖 The 19 Agents

### — Original 8 Agents —

#### 1. 📝 Caption Agent
Auto-generate broadcast-ready captions with QA validation.
- **Demo:** Mock transcription segments with confidence scores
- **Production:** OpenAI Whisper API + speaker diarization
- **API:** `POST /api/caption/process`
- **Slack:** `/miq-caption [url]`

#### 2. 🎬 Clip Agent
Detect viral moments from broadcasts using AI vision analysis.
- **Demo:** Preset viral moments with scores and hashtags
- **Production:** GPT-4 Vision frame-by-frame analysis
- **API:** `POST /api/clip/process`
- **Slack:** `/miq-clip [url]`

#### 3. ⚖️ Compliance Agent
24/7 FCC compliance monitoring. Rules: 47 U.S.C. § 326, § 315, § 317, 47 CFR Part 11.
- **Demo:** Randomised issue sets with severity levels
- **Production:** Whisper transcription + AI content analysis
- **API:** `POST /api/compliance/scan`
- **Slack:** `/miq-compliance [url]`

#### 4. 🔍 Archive Agent
Natural language search with MAM system integration.
- **Demo:** Mock asset library with AI tagging
- **Production:** Avid Media Central API connector
- **API:** `POST /api/archive/search`
- **Slack:** `/miq-archive [query]`

#### 5. 📱 Social Publishing Agent
Generate platform-optimised posts for Twitter/X, Instagram, TikTok, Facebook, YouTube Shorts.
- **API:** `POST /api/social/generate`
- **Slack:** `/miq-social [url]`

#### 6. 🌍 Localization Agent
Translate captions and generate AI voice dubs via ElevenLabs. 8 languages supported.
- **API:** `POST /api/localization/translate`
- **Slack:** `/miq-localize [url] --language=es`

#### 7. 📜 Rights Agent
Track licenses, detect violations, automate DMCA. Alerts at 90/60/30 days pre-expiry.
- **API:** `POST /api/rights/check`
- **Slack:** `/miq-rights`

#### 8. 📈 Trending Agent
Real-time trend monitoring from social, news wires, and Google Trends. Velocity scoring.
- **API:** `POST /api/trending/monitor`
- **Slack:** `/miq-trending [--live] [--topic=X]`

---

### — Future-Ready 6 Agents —

#### 9. 🕵️ Deepfake Detection Agent
**Market Gap:** 900% growth in AI synthetic media. No broadcast vendor offers real-time forensic detection.

- 3-layer analysis: audio spectral, video facial consistency, C2PA metadata provenance
- Risk levels: `authentic` → `suspicious` → `likely_fake` → `confirmed_fake`
- Auto-hold from broadcast when score > `DEEPFAKE_RISK_THRESHOLD` (default 0.60)
- **Slack:** `/miq-deepfake [url]` → card with Release/Reject buttons

#### 10. ✅ Live Fact-Check Agent
**Market Gap:** No real-time claim verification integrated into the live broadcast chain.

- 8 databases: AP, Reuters, PolitiFact, FactCheck.org, Snopes, Full Fact, IFCN, WHO
- Verdicts: `true` → `mostly_true` → `half_true` → `misleading` → `false` → `unverified` → `outdated`
- Auto-alert anchor producers on false/misleading claims
- **Slack:** `/miq-factcheck [text]` → card with Alert Anchor button

#### 11. 📊 Audience Intelligence Agent
**Market Gap:** Nielsen/Comscore measure past performance. No tool predicts second-by-second retention live.

- Second-by-second retention curve prediction
- Drop-off risk alerts (threshold: 4% drop per segment)
- 6 demographic bands: 18-24, 25-34, 35-44, 45-54, 55-64, 65+
- **Slack:** `/miq-audience` → retention curve card

#### 12. 🎬 AI Production Director Agent
**Market Gap:** No AI system autonomously orchestrates cameras, lower-thirds, rundown, and commercial breaks.

- Camera shot plan, lower-thirds generation, rundown optimisation, break timing
- `PRODUCTION_DIRECTOR_AUTO_ACCEPT=false` (default) — human approval required
- **Slack:** `/miq-production` → card with Approve/Reject buttons

#### 13. 🛡️ Brand Safety Agent
**Market Gap:** No broadcast tool scores content contextually in real-time for dynamic ad insertion.

- GARM 10-category risk detection + IAB Tech Lab 36-category taxonomy
- 6 advertiser profiles with CPM modifiers
- Auto-block premium ad insertion on GARM critical flags
- **Slack:** `/miq-brand [url]` → safety score card with Override/Block buttons

#### 14. 🌿 Carbon Intelligence Agent
**Market Gap:** No broadcast vendor tracks production carbon footprint. ESG reporting is entirely manual.

- GHG Protocol Scope 1/2/3 tracking across 12 equipment profiles
- 9 regional electricity grids with live carbon intensity
- GRI 305 / TCFD / GHG Protocol aligned ESG reports
- **Slack:** `/miq-carbon` → ESG metrics card

---

### — Phase 1 Pipeline Agents (NEW in v3.1) —

#### 15. 📥 Ingest & Transcode Agent
**Pipeline Stage:** Ingest — the front door of the broadcast pipeline.

- **Inputs:** File-based (S3, local, FTP), live feeds (RTMP, SRT, HLS), SDI-over-IP
- **Output Profiles:** `broadcast_hd` (MXF H.264 50Mbps), `broadcast_4k` (MXF H.265 150Mbps), `ott_hls` (fMP4 8Mbps), `proxy_edit` (ProRes 45Mbps), `web_mp4`, `thumbnail`
- **Demo:** Realistic mock ingest job with all output profiles
- **Production:** Local FFmpeg or AWS MediaConvert (configurable via `INGEST_USE_CLOUD`)
- **Slack:** `/miq-ingest [source_url]` → ingest report with "Process All Agents" button
- **Event trigger:** Fires `NEW_CONTENT` event → chains Caption + Clip + Compliance + Deepfake + Brand Safety

#### 16. 📡 Signal Quality Monitor Agent
**Pipeline Stage:** Production — real-time broadcast quality assurance.

- **Audio:** EBU R128 / ATSC A/85 loudness (LUFS), true peak (dBTP), loudness range (LU)
- **Video:** Black frame detection, freeze frame detection, blockiness scoring
- **Compliance Standards:** EBU R128 (-23 LUFS ±1), ATSC A/85 (-24 LUFS), true peak -1.0 dBTP
- **Demo:** Realistic QC scenarios (clean / warning / critical) with randomised issues
- **Production:** FFmpeg ffprobe + loudnorm filter for real measurement
- **Alerts:** Critical issues trigger Slack/Teams NOC alert automatically
- **Slack:** `/miq-signal [stream_url]` → QC card with Auto-Correct / Alert NOC buttons
- **Schedule:** Every 2 minutes

#### 17. 📺 Playout & Scheduling Agent
**Pipeline Stage:** Distribution — linear broadcast schedule management.

- **Automation Systems:** Harmonic Polaris, GV Maestro, Ross Overdrive (REST API)
- **Features:** Full 24h schedule view, SCTE-35 ad break injection, schedule warnings, on-air item tracking
- **Demo:** Realistic mock schedule with 12 items, break timings, and warnings
- **Production:** Connects to `AUTOMATION_SERVER_URL` REST API
- **Slack:** `/miq-playout` → schedule card with Approve/Push to Automation buttons
- **Schedule:** Every 5 minutes

#### 18. 🌐 OTT / Multi-Platform Distribution Agent
**Pipeline Stage:** Distribution — streaming platform management.

- **Packaging:** HLS (6-second segments) + DASH (4-second segments)
- **ABR Ladder:** 4K HDR → 1080p High → 1080p → 720p → 480p → 360p → audio-only
- **CDN:** CloudFront, Akamai, Fastly (configurable via `CDN_PROVIDER`)
- **Platforms:** YouTube Data API, Meta Graph API (VOD publishing)
- **Demo:** Realistic mock with HLS/DASH URLs, CDN health, ABR profiles
- **Production:** AWS MediaPackage + CloudFront / Akamai APIs
- **Slack:** `/miq-ott [url]` → distribution card with CDN URLs and analytics button
- **Schedule:** Every 10 minutes (CDN health check)

#### 19. 📰 Newsroom Integration Agent
**Pipeline Stage:** Pre-production → Production bridge.

- **Newsroom Systems:** iNews, ENPS, Octopus (via REST API + MOS protocol)
- **Wire Services:** AP, Reuters, AFP, Bloomberg, PA Media ingestion
- **Features:** Full rundown sync, story status tracking, MOS object management, wire story assignment, breaking news detection
- **Demo:** Realistic mock rundown with 8 stories, wire feeds, and urgent story flags
- **Production:** iNews REST API at `INEWS_API_URL`
- **Slack:** `/miq-newsroom` → rundown card with Sync / Push to Playout buttons
- **Schedule:** Every 3 minutes

---

## 🔌 Connector Framework

### Architecture

```python
BaseConnector (abstract)
  ├── authenticate()        # establish connection
  ├── health_check()        # verify liveness → HealthCheckResult
  ├── read(params)          # pull data from system
  ├── write(data, params)   # push data to system
  ├── subscribe(event, cb)  # event streaming (webhooks/WS)
  └── get_tool_definitions() # MCP-style tool schema

ConnectorRegistry
  ├── register(connector)           # add to registry + index tools
  ├── get(connector_id)             # look up by ID
  ├── get_by_category(category)     # all connectors in a category
  ├── connect_all()                 # authenticate all concurrently
  ├── health_check_all()            # run health checks concurrently
  ├── get_all_tool_definitions()    # MCP tool discovery
  └── call_tool(tool_name, input)   # MCP tool execution
```

### ConnectorCategory Enum

| Category | Systems |
|----------|---------|
| `COMMS` | Slack, Teams |
| `STORAGE` | AWS S3, Azure Blob, local NAS |
| `MAM` | Avid Media Central, Frame.io, Dalet |
| `NEWSROOM` | iNews, ENPS, Octopus, AP Wire |
| `PLAYOUT` | Harmonic Polaris, GV Maestro |
| `CDN` | Akamai, CloudFront, Fastly |
| `TRANSCODING` | FFmpeg, AWS MediaConvert |
| `ADTECH` | FreeWheel, Google Ad Manager |
| `ANALYTICS` | Nielsen, Comscore |
| `MONITORING` | Datadog, PagerDuty, Nagios |
| `SOCIAL` | YouTube, Meta, Twitter/X |
| `NLE` | Adobe Premiere, DaVinci Resolve |

### MCP Tool Definitions

Each connector declares its capabilities as typed tool schemas:

```python
class SlackChannelConnector(BaseConnector):
    def get_tool_definitions(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="slack_send_message",
                description="Send a message or Block Kit card to a Slack channel",
                input_schema={
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string"},
                        "text":    {"type": "string"},
                        "blocks":  {"type": "array"},
                    },
                    "required": ["channel"],
                },
                connector_id="slack",
                operation="write",
            ),
        ]
```

Agents call connectors through the registry without coupling to specific implementations:

```python
# In any agent:
result = await connector_registry.call_tool(
    "slack_send_alert",
    {"title": "Deepfake Detected", "message": "Content held", "severity": "critical"}
)
```

### Currently Available MCP Tools (v3.1)

| Tool | Connector | Operation |
|------|-----------|-----------|
| `slack_send_message` | Slack | write |
| `slack_send_alert` | Slack | write |
| `slack_read_channel` | Slack | read |
| `teams_send_message` | Teams | write |
| `teams_send_alert` | Teams | write |

---

## 🤖 Autonomous Orchestrator

### Scheduled Jobs (14 total)

| Job ID | Agent | Interval | Purpose |
|--------|-------|----------|---------|
| `production_director_live` | AI Production Director | 60s | Live production cues |
| `deepfake_monitor` | Deepfake Detection | 120s | Scan incoming content |
| `brand_safety_monitor` | Brand Safety | 120s | Segment ad safety scoring |
| `signal_quality_monitor` | Signal Quality | 120s | Live stream QC |
| `fact_check_live` | Live Fact-Check | 180s | Verify live captions |
| `newsroom_sync` | Newsroom Integration | 180s | Rundown refresh |
| `trending_monitor` | Trending | 300s | Trend monitoring |
| `audience_live` | Audience Intelligence | 300s | Retention prediction |
| `playout_refresh` | Playout & Scheduling | 300s | Schedule refresh |
| `compliance_monitor` | Compliance | 600s | FCC monitoring |
| `ott_health` | OTT Distribution | 600s | CDN health check |
| `rights_monitor` | Rights | 3600s | License expiry checks |
| `carbon_monitor` | Carbon Intelligence | 1800s | ESG metric updates |
| `archive_optimize` | Archive | 21600s | Index optimisation |

### Event System

| Event | Fired By | Subscribing Agents |
|-------|----------|--------------------|
| `NEW_CONTENT` | File upload / Ingest | Caption, Clip, Compliance, Archive, Deepfake, Brand Safety, Audience |
| `CAPTION_COMPLETE` | Caption Agent | Localization, Social, Live Fact-Check |
| `CLIP_DETECTED` | Clip Agent | Social Publishing |
| `COMPLIANCE_ALERT` | Compliance Agent | Notification system |
| `TRENDING_SPIKE` | Trending Agent | Social, Archive |
| `LICENSE_EXPIRING` | Rights Agent | Alert system |
| `VIOLATION_DETECTED` | Rights Agent | Rights Agent |
| `BREAKING_NEWS` | Trending Agent | Social, Trending, AI Production Director, Live Fact-Check |

### Task Priority Queue

```python
class TaskPriority(Enum):
    CRITICAL = 1  # Compliance violations, deepfake detection on new uploads
    HIGH     = 2  # Brand safety, expiring licenses, compliance scans
    NORMAL   = 3  # Caption, clip, localization, audience, OTT, newsroom
    LOW      = 4  # Archive indexing, background optimization
```

---

## ⚙️ Full Configuration Reference

```bash
# ─── Mode ─────────────────────────────────────────────────
PRODUCTION_MODE=false           # true = real APIs, false = demo mode

# ─── AI Services ──────────────────────────────────────────
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_WHISPER_MODEL=whisper-1
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# ─── Slack Bot ────────────────────────────────────────────
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_DEFAULT_CHANNEL=#mediaagentiq

# ─── Microsoft Teams Bot ──────────────────────────────────
TEAMS_APP_ID=...
TEAMS_APP_PASSWORD=...
TEAMS_TENANT_ID=common

# ─── MAM Integration ──────────────────────────────────────
AVID_HOST=https://your-avid-server/api
AVID_USERNAME=api_user
AVID_PASSWORD=...
AVID_WORKSPACE=default
AVID_MOCK_MODE=true

# ─── NMOS Integration ─────────────────────────────────────
NMOS_REGISTRY_URL=http://nmos-registry:8080
NMOS_NODE_ID=mediaagentiq-node-001
NMOS_ENABLED=false

# ─── Phase 1 — Ingest & Transcode ─────────────────────────
INGEST_DEFAULT_PROFILES=broadcast_hd,proxy_edit,web_mp4
INGEST_USE_CLOUD=false
AWS_MEDIACONVERT_ENDPOINT=...
AWS_MEDIACONVERT_ROLE_ARN=...

# ─── Phase 1 — Signal Quality ─────────────────────────────
SIGNAL_QUALITY_LOUDNESS_TARGET_LUFS=-23.0
SIGNAL_QUALITY_TRUE_PEAK_LIMIT=-1.0
SIGNAL_QUALITY_ALERT_ON_CRITICAL=true

# ─── Phase 1 — Playout ────────────────────────────────────
AUTOMATION_SERVER_URL=http://harmonic-server/api
AUTOMATION_SERVER_TYPE=harmonic         # harmonic | gv_maestro | ross_overdrive

# ─── Phase 1 — OTT Distribution ───────────────────────────
CDN_PROVIDER=cloudfront                 # cloudfront | akamai | fastly
CDN_ORIGIN_URL=https://origin.example.com
OTT_DRM_ENABLED=false
AWS_MEDIAPACKAGE_CHANNEL_ID=...

# ─── Phase 1 — Newsroom ───────────────────────────────────
INEWS_API_URL=http://inews-server/api
ENPS_API_URL=http://enps-server/api
NEWSROOM_SYNC_INTERVAL_SECS=180

# ─── Future-Ready Agent Settings ──────────────────────────
DEEPFAKE_RISK_THRESHOLD=0.60
DEEPFAKE_AUTO_HOLD=true
DEEPFAKE_SENSITIVITY=balanced
FACT_CHECK_AUTO_ALERT=true
FACT_CHECK_CLAIM_MIN_CONFIDENCE=0.70
FACT_CHECK_DATABASES=ap,reuters,politifact,factcheck_org,snopes
AUDIENCE_PREDICTION_INTERVAL_SECS=300
AUDIENCE_DROP_OFF_ALERT_THRESHOLD=0.04
PRODUCTION_DIRECTOR_AUTO_ACCEPT=false
PRODUCTION_DIRECTOR_CAMERA_LATENCY_MS=500
BRAND_SAFETY_DEFAULT_FLOOR=70
BRAND_SAFETY_AUTO_BLOCK=true
BRAND_SAFETY_GARM_ENABLED=true
CARBON_GRID_REGION=US_Northeast
CARBON_ESG_REPORT_ENABLED=true
CARBON_RENEWABLE_PPA=0.0
CARBON_REPORTING_INTERVAL_SECS=1800

# ─── Database ─────────────────────────────────────────────
DATABASE_URL=sqlite+aiosqlite:///mediaagentiq.db

# ─── Server ───────────────────────────────────────────────
HOST=127.0.0.1
PORT=8000
DEBUG=true
```

---

## 🌐 API Reference

### FastAPI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/gateway/health` | Gateway health + active sessions |
| POST | `/slack/events` | Slack Events API (app_mention, message) |
| POST | `/slack/commands` | Slack slash commands (/miq-*) |
| POST | `/slack/actions` | Slack interactive component callbacks |
| POST | `/teams/messages` | Teams Bot Framework Activity |
| POST | `/api/caption/process` | Generate captions |
| POST | `/api/clip/process` | Detect viral clips |
| POST | `/api/archive/search` | Search archive |
| POST | `/api/compliance/scan` | Compliance scan |
| POST | `/api/social/generate` | Generate social posts |
| POST | `/api/localization/translate` | Translate content |
| POST | `/api/rights/check` | Check licenses |
| POST | `/api/trending/monitor` | Monitor trends |
| GET | `/api/stats` | Dashboard stats |
| GET | `/api/activity` | Recent activity |

---

## 🔵 Slack Bot Setup

1. Go to https://api.slack.com/apps → **Create New App**
2. **Event Subscriptions** → Enable → Request URL: `https://your-domain/slack/events`
   - Subscribe to: `app_mention`, `message.channels`
3. **Slash Commands** → Create commands pointing to `https://your-domain/slack/commands`:
   - `/miq-compliance`, `/miq-trending`, `/miq-deepfake`, `/miq-status`, `/miq-help`, etc.
4. **Interactivity & Shortcuts** → Request URL: `https://your-domain/slack/actions`
5. **OAuth & Permissions** → Bot Token Scopes: `chat:write`, `channels:history`, `commands`
6. Install to workspace → copy **Bot User OAuth Token** and **Signing Secret** to `.env`

## 🟦 Teams Bot Setup

1. **Azure Portal** → Create a Bot Channels Registration
2. Set Messaging Endpoint: `https://your-domain/teams/messages`
3. Add Microsoft Teams channel
4. Copy **App ID** and **Password** (client secret) to `.env`
5. Distribute via Teams App Manifest or direct link

---

## 📁 Full Project Structure

```
MediaAgentIQ/
├── streamlit_app.py               # Streamlit UI (19 agent pages)
├── orchestrator.py                # Autonomous Orchestrator (19 agents, 14 jobs)
├── app.py                         # FastAPI + gateway mount
├── settings.py                    # Pydantic config (60+ typed settings)
├── config.py                      # Legacy config
├── database.py                    # SQLite async
├── requirements.txt
├── .env.example
│
├── gateway/                       # Conversational Gateway (NEW v3.1)
│   ├── __init__.py
│   ├── router.py                  # slash + NLP + LLM routing
│   ├── formatter.py               # Block Kit + Adaptive Card formatters for all 19 agents
│   ├── conversation.py            # Per-user multi-turn context (30-min TTL)
│   └── webhook_handler.py         # /slack/* and /teams/* FastAPI routes
│
├── connectors/                    # MCP Connector Framework (NEW v3.1)
│   ├── __init__.py                # setup_connectors() startup helper
│   ├── base_connector.py          # BaseConnector, ToolDefinition, HealthCheckResult
│   ├── registry.py                # ConnectorRegistry with call_tool() MCP dispatch
│   └── channels/                  # User-facing channel connectors
│       ├── __init__.py
│       ├── slack.py               # Slack Bot (Block Kit, alerts, updates)
│       └── teams.py               # Teams Bot (Adaptive Cards, proactive)
│
├── agents/                        # 19 AI Agents
│   ├── __init__.py                # AGENTS registry dict + all exports
│   ├── base_agent.py              # BaseAgent (dual-mode, create_response)
│   │
│   │   — Original 8 —
│   ├── caption_agent.py
│   ├── clip_agent.py
│   ├── compliance_agent.py
│   ├── archive_agent.py
│   ├── social_publishing_agent.py
│   ├── localization_agent.py
│   ├── rights_agent.py
│   ├── trending_agent.py
│   │
│   │   — Future-Ready 6 —
│   ├── deepfake_detection_agent.py
│   ├── live_fact_check_agent.py
│   ├── audience_intelligence_agent.py
│   ├── ai_production_director_agent.py
│   ├── brand_safety_agent.py
│   ├── carbon_intelligence_agent.py
│   │
│   │   — Phase 1 Pipeline 5 (NEW v3.1) —
│   ├── ingest_transcode_agent.py
│   ├── signal_quality_agent.py
│   ├── playout_scheduling_agent.py
│   ├── ott_distribution_agent.py
│   └── newsroom_integration_agent.py
│
├── services/                      # AI Service Wrappers
│   ├── transcription.py           # Whisper API
│   ├── vision.py                  # GPT-4 Vision
│   └── dubbing.py                 # ElevenLabs
│
├── integrations/                  # Broadcast System Integrations
│   ├── avid/                      # Avid Media Central (MAM)
│   └── grass_valley/              # NMOS IS-04/IS-05
│
├── templates/                     # FastAPI Jinja2 HTML
├── static/                        # CSS + JS
├── uploads/                       # User uploads
└── outputs/                       # Generated files
```

---

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 8501
CMD ["sh", "-c", "streamlit run streamlit_app.py & uvicorn app:app --host 0.0.0.0"]
```

### Production Recommendations

1. **Reverse Proxy:** Nginx/Caddy for HTTPS (required for Slack/Teams webhooks)
2. **Database:** PostgreSQL for production scale
3. **Cache:** Redis for session/conversation context
4. **Queue:** Redis/RabbitMQ for task queue at scale
5. **Monitoring:** Prometheus + Grafana
6. **Logging:** ELK Stack or CloudWatch

---

## 📈 Changelog

### v3.1.0 — Pipeline + Channel Edition
- ✅ Conversational Gateway (`gateway/`) — NLP + slash routing, Block Kit/Adaptive Card formatting, multi-turn context
- ✅ Slack Bot integration — full webhook handler, 17 slash commands, interactive button callbacks
- ✅ Microsoft Teams Bot — Adaptive Cards, proactive messaging, Bot Framework auth
- ✅ MCP Connector Framework — BaseConnector, ConnectorRegistry, ToolDefinition, call_tool()
- ✅ 5 Slack/Teams MCP tools registered at startup
- ✅ IngestTranscodeAgent — 6 output profiles, FFmpeg + AWS MediaConvert
- ✅ SignalQualityAgent — EBU R128, true peak, black frame, freeze, NOC alerts
- ✅ PlayoutSchedulingAgent — Harmonic/GV Maestro, SCTE-35, 24h schedule
- ✅ OTTDistributionAgent — HLS/DASH, 7-rung ABR ladder, CloudFront/Akamai
- ✅ NewsroomIntegrationAgent — iNews/ENPS MOS, wire ingestion, rundown sync
- ✅ 4 new autonomous scheduled jobs (signal: 2min, newsroom: 3min, playout: 5min, OTT: 10min)
- ✅ All 19 agents in AGENTS registry, all 19 in orchestrator, 14 scheduled jobs

### v3.0.0 — Future-Ready Edition
- ✅ 6 future-ready agents (Deepfake, Fact-Check, Audience, Production Director, Brand Safety, Carbon)
- ✅ Extended orchestrator, extended settings.py, updated Streamlit UI

### v2.0.0
- ✅ Autonomous Orchestrator, All-in-One Workflow, MAM + NMOS integrations

### v1.0.0
- ✅ Initial release — 8 agents, FastAPI, basic Streamlit UI

---

*Last Updated: February 2026 | MediaAgentIQ v3.1.0*
