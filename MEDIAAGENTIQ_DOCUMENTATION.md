# MediaAgentIQ v2.0 - Complete Documentation

## 📋 Overview

MediaAgentIQ is an enterprise AI-powered agent platform for media and broadcast organizations. It provides **8 specialized AI agents** that run **autonomously** to automate critical workflows - from captioning to compliance monitoring, viral clip detection to rights management.

**Key Features:**
- 🤖 **Autonomous Operation** - Agents run 24/7 without manual intervention
- 🔄 **Dual-Mode Architecture** - Demo mode for showcasing, Production mode with real AI
- 🚀 **All-in-One Workflow** - Process through all 8 agents simultaneously
- 🔌 **Enterprise Integrations** - MAM, NMOS, broadcast automation connectivity
- ⚡ **Event-Driven** - Agents trigger each other automatically

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

```bash
# Clone/navigate to project
cd MediaAgentIQ

# Install dependencies
pip install -r requirements.txt

# Option 1: Run Streamlit UI (Recommended for demos)
streamlit run streamlit_app.py

# Option 2: Run FastAPI backend
uvicorn app:app --reload

# Option 3: Run Autonomous Orchestrator
python orchestrator.py
```

### Access Points
- **Streamlit UI:** http://localhost:8501
- **FastAPI Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MediaAgentIQ Platform                              │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Presentation Layer                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   │  │
│  │  │  Streamlit  │  │   FastAPI   │  │  WebSocket  │                   │  │
│  │  │     UI      │  │   Backend   │  │   Events    │                   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Autonomous Orchestrator Layer                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │  │
│  │  │  Task Queue  │  │  Scheduler   │  │ Event System │                │  │
│  │  │  (Priority)  │  │  (Periodic)  │  │  (Triggers)  │                │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                          Agent Layer (8 Agents)                        │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                     │  │
│  │  │ Caption │ │  Clip   │ │Compliance│ │ Archive │                     │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘                     │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                     │  │
│  │  │ Social  │ │ Local-  │ │ Rights  │ │Trending │                     │  │
│  │  │   Pub   │ │ ization │ │  Agent  │ │  Agent  │                     │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                          Services Layer                                │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐          │  │
│  │  │  Transcription │  │     Vision     │  │    Dubbing     │          │  │
│  │  │  (Whisper AI)  │  │  (GPT-4 Vision)│  │  (ElevenLabs)  │          │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                       Integrations Layer                               │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌───────┐ ┌──────┐ ┌────────┐           │  │
│  │  │ Avid │ │ NMOS │ │ AWS  │ │Social │ │ MOS  │ │Database│           │  │
│  │  │ MAM  │ │IS-04 │ │Azure │ │ APIs  │ │Proto │ │ SQLite │           │  │
│  │  └──────┘ └──────┘ └──────┘ └───────┘ └──────┘ └────────┘           │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Dual-Mode Processing

Every agent supports two modes:

```python
class BaseAgent:
    async def process(self, input_data):
        if self.is_production_mode:
            return await self._production_process(input_data)  # Real AI
        else:
            return await self._demo_process(input_data)  # Mock data
```

---

## 🤖 The 8 AI Agents

### 1. 📝 Caption Agent

**Purpose:** Auto-generate broadcast-ready captions with QA validation

**Capabilities:**
| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| Transcription | Mock data | Whisper AI |
| Speaker Diarization | Simulated | AI-detected |
| Confidence Scoring | Random | Real scores |
| QA Validation | Preset issues | AI analysis |
| Export Formats | SRT, VTT, JSON | SRT, VTT, JSON |

**API:** `POST /api/caption/process`

**Production Integration:**
```python
# Uses OpenAI Whisper
from services.transcription import TranscriptionService
service = TranscriptionService(settings)
result = await service.transcribe(audio_path)
```

---

### 2. 🎬 Clip Agent

**Purpose:** Detect viral moments from broadcasts using AI vision analysis

**Capabilities:**
| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| Scene Analysis | Preset clips | GPT-4 Vision |
| Emotion Detection | Mock scores | AI face analysis |
| Viral Scoring | Random 0.8-0.99 | Multi-factor AI |
| Hashtag Generation | Preset tags | AI-generated |
| Platform Optimization | Fixed list | Trend-aware |

**API:** `POST /api/clip/process`

**Production Integration:**
```python
# Uses GPT-4 Vision
from services.vision import VisionService
service = VisionService(settings)
analysis = await service.analyze_frame(frame_path, "Detect viral moments")
```

---

### 3. ⚖️ Compliance Agent

**Purpose:** 24/7 FCC compliance monitoring with violation detection

**Capabilities:**
| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| Profanity Detection | Preset issues | Whisper + AI |
| Political Ad Check | Mock alerts | Content analysis |
| Sponsorship ID | Simulated | Vision detection |
| EAS Compliance | Preset status | Real validation |
| Risk Scoring | Fixed score | AI-calculated |

**FCC Rules Monitored:**
- 47 U.S.C. § 326 - Indecent Content
- 47 U.S.C. § 315 - Political Broadcasting
- 47 U.S.C. § 317 - Sponsorship Identification
- 47 CFR Part 11 - Emergency Alert System

**API:** `POST /api/compliance/scan`

---

### 4. 🔍 Archive Agent

**Purpose:** Natural language search with MAM system integration

**Capabilities:**
| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| NL Query Parsing | Keyword match | AI semantic |
| Search Results | Mock archive | MAM API query |
| AI Tagging | Preset tags | GPT analysis |
| Metadata Sync | Simulated | Bi-directional |

**MAM Integration:**
```python
# Avid Media Central connector
from integrations.avid import AvidConnector
connector = AvidConnector(settings)
assets = await connector.search_assets(query)
```

**API:** `POST /api/archive/search`

---

### 5. 📱 Social Publishing Agent

**Purpose:** Generate platform-optimized social media posts

**Supported Platforms:**
| Platform | Max Chars | Optimization |
|----------|-----------|--------------|
| Twitter/X | 280 | Hashtags, threads |
| Instagram | 2,200 | Emojis, multi-image |
| TikTok | 150 | Trending sounds |
| Facebook | 63,206 | Long-form, video |
| YouTube Shorts | 100 | SEO keywords |

**API:** `POST /api/social/generate`

---

### 6. 🌍 Localization Agent

**Purpose:** Translate captions and generate AI voice dubs

**Supported Languages:**
| Language | Translation | Voice Dubbing |
|----------|-------------|---------------|
| Spanish | ✅ | ✅ ElevenLabs |
| French | ✅ | ✅ ElevenLabs |
| German | ✅ | ✅ ElevenLabs |
| Chinese | ✅ | ✅ ElevenLabs |
| Japanese | ✅ | ✅ ElevenLabs |
| Arabic | ✅ | ✅ ElevenLabs |
| Hindi | ✅ | ✅ ElevenLabs |
| Portuguese | ✅ | ✅ ElevenLabs |

**Production Integration:**
```python
# ElevenLabs dubbing
from services.dubbing import DubbingService
service = DubbingService(settings)
audio = await service.generate_dub(text, voice_id, language)
```

**API:** `POST /api/localization/translate`

---

### 7. 📜 Rights Agent

**Purpose:** Track licenses, detect violations, automate DMCA

**Capabilities:**
| Feature | Description |
|---------|-------------|
| License Tracking | Expiry alerts at 90/60/30 days |
| Violation Detection | Platform monitoring + Content ID |
| DMCA Automation | Auto-generate takedown requests |
| Cost Analysis | Track licensing spend |
| Compliance Scoring | Per-license compliance % |

**API:** `POST /api/rights/check`

---

### 8. 📈 Trending Agent

**Purpose:** Real-time trend monitoring and breaking news alerts

**Data Sources:**
- Social media (Twitter/X, TikTok, Reddit)
- News wires (AP, Reuters, AFP)
- Google Trends
- Custom RSS feeds

**Metrics Tracked:**
| Metric | Description |
|--------|-------------|
| Velocity Score | How fast topic is growing (0-100) |
| Volume | Posts/mentions per hour |
| Sentiment | Positive/Negative/Mixed |
| Demographics | Age group breakdown |

**API:** `POST /api/trending/monitor`

---

## 🤖 Autonomous Orchestrator

### Overview

The `orchestrator.py` provides autonomous background execution:

```python
from orchestrator import start_autonomous_agents

# Start all agents running autonomously
await start_autonomous_agents()
```

### Scheduled Jobs

| Agent | Interval | Purpose |
|-------|----------|---------|
| Trending | 5 min | Monitor trends, detect breaking news |
| Compliance | 10 min | Continuous FCC monitoring |
| Rights | 1 hour | License expiration checks |
| Archive | 6 hours | Index optimization |

### Event System

Events trigger automatic agent execution:

| Event | Triggered By | Triggers Agents |
|-------|--------------|-----------------|
| `NEW_CONTENT` | File upload | Caption, Clip, Compliance, Archive |
| `CAPTION_COMPLETE` | Caption Agent | Localization, Social |
| `CLIP_DETECTED` | Clip Agent | Social Publishing |
| `COMPLIANCE_ALERT` | Compliance Agent | Notification system |
| `TRENDING_SPIKE` | Trending Agent | Social, Archive |
| `LICENSE_EXPIRING` | Rights Agent | Alert system |
| `BREAKING_NEWS` | Trending Agent | Social, Trending |

### Task Queue

Priority-based processing:

```python
class TaskPriority(Enum):
    CRITICAL = 1  # Compliance violations, breaking news
    HIGH = 2      # Expiring licenses, trending alerts
    NORMAL = 3    # Regular processing
    LOW = 4       # Background optimization
```

### Usage

```python
from orchestrator import orchestrator

# Submit a task
task_id = orchestrator.submit_task(
    agent_type=AgentType.CAPTION,
    input_data="/path/to/video.mp4",
    priority=TaskPriority.NORMAL
)

# Check status
status = orchestrator.get_task_status(task_id)

# Submit content for all agents
task_ids = submit_content_for_processing("/path/to/video.mp4", run_all=True)
```

---

## 🔌 Integrations

### Media Asset Management (MAM)

**Avid Media Central Integration:**
```python
from integrations.avid import AvidConnector, AvidAuth

# Authenticate
auth = AvidAuth(settings)
token = await auth.get_token()

# Connect
connector = AvidConnector(settings)
await connector.connect()

# Search assets
assets = await connector.search_assets("election coverage")

# Get asset metadata
metadata = await connector.get_asset_metadata(asset_id)
```

### NMOS IP Infrastructure

**Grass Valley NMOS Client (IS-04/IS-05):**
```python
from integrations.grass_valley import NMOSClient

client = NMOSClient(settings)

# Discover devices
devices = await client.discover_devices()

# Get senders/receivers
senders = await client.get_senders()
receivers = await client.get_receivers()

# Make connection
await client.make_connection(sender_id, receiver_id)
```

### Supported Protocols

| Protocol | Use Case |
|----------|----------|
| REST API | MAM, Cloud services |
| MOS Protocol | Broadcast automation |
| NMOS IS-04 | Device discovery |
| NMOS IS-05 | Connection management |
| WebSocket | Real-time updates |
| Webhooks | External notifications |

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# ===================
# Mode Configuration
# ===================
PRODUCTION_MODE=false          # true = real AI, false = demo mode

# ===================
# AI Services
# ===================
OPENAI_API_KEY=sk-...         # Required for production mode
OPENAI_MODEL=gpt-4-turbo-preview
WHISPER_MODEL=whisper-1

ELEVENLABS_API_KEY=...        # For voice dubbing
ELEVENLABS_VOICE_ID=...       # Default voice

# ===================
# MAM Integration
# ===================
AVID_API_URL=https://your-avid-server/api
AVID_USERNAME=api_user
AVID_PASSWORD=...
AVID_WORKSPACE_ID=default

# ===================
# NMOS Integration
# ===================
NMOS_REGISTRY_URL=http://nmos-registry:8080
NMOS_NODE_ID=mediaagentiq-node-001

# ===================
# Database
# ===================
DATABASE_URL=sqlite:///./mediaagentiq.db
```

### Settings (settings.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Mode
    PRODUCTION_MODE: bool = False

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # ElevenLabs
    ELEVENLABS_API_KEY: str = ""

    # Computed properties
    @property
    def is_openai_configured(self) -> bool:
        return bool(self.OPENAI_API_KEY)

    class Config:
        env_file = ".env"
```

---

## 📁 Project Structure

```
MediaAgentIQ/
├── streamlit_app.py          # Streamlit UI (2400+ lines)
├── orchestrator.py           # Autonomous Agent Orchestrator (580+ lines)
├── app.py                    # FastAPI Backend
├── settings.py               # Pydantic Configuration
├── config.py                 # Legacy config
├── database.py               # SQLite async setup
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
│
├── agents/                   # AI Agent Implementations
│   ├── __init__.py          # Exports all agents
│   ├── base_agent.py        # Dual-mode base class
│   ├── caption_agent.py     # Transcription + QA
│   ├── clip_agent.py        # Viral detection
│   ├── compliance_agent.py  # FCC monitoring
│   ├── archive_agent.py     # MAM search
│   ├── social_publishing_agent.py  # Social posts
│   ├── localization_agent.py       # Translation + dubbing
│   ├── rights_agent.py      # License management
│   └── trending_agent.py    # Trend monitoring
│
├── services/                 # AI Service Wrappers
│   ├── __init__.py
│   ├── transcription.py     # Whisper API wrapper
│   ├── vision.py            # GPT-4 Vision wrapper
│   └── dubbing.py           # ElevenLabs wrapper
│
├── integrations/             # External System Integrations
│   ├── __init__.py
│   ├── base.py              # Base integration class
│   ├── avid/                # Avid Media Central
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication
│   │   ├── connector.py     # API connector
│   │   └── models.py        # Data models
│   └── grass_valley/        # NMOS Integration
│       ├── __init__.py
│       └── nmos_client.py   # IS-04/IS-05 client
│
├── templates/                # FastAPI HTML templates (9 pages)
├── static/                   # CSS & JavaScript
├── uploads/                  # User uploads (auto-created)
└── outputs/                  # Generated files (auto-created)
```

---

## 🌐 API Reference

### Base URL
```
FastAPI: http://localhost:8000
Streamlit: http://localhost:8501
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| POST | `/api/caption/process` | Generate captions |
| POST | `/api/clip/process` | Detect viral clips |
| POST | `/api/archive/search` | Search archive |
| POST | `/api/compliance/scan` | Compliance scan |
| POST | `/api/social/generate` | Generate posts |
| POST | `/api/localization/translate` | Translate content |
| POST | `/api/rights/check` | Check licenses |
| POST | `/api/trending/monitor` | Monitor trends |
| GET | `/api/stats` | Dashboard stats |
| GET | `/api/activity` | Recent activity |

### WebSocket Events (Planned)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Handle: task_complete, compliance_alert, trending_spike, etc.
};
```

---

## 🗄️ Database Schema

### Tables

```sql
-- Jobs tracking
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    agent_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    input_file TEXT,
    output_file TEXT,
    result_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Archive content
CREATE TABLE archive (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    duration INTEGER,
    date_recorded DATE,
    tags TEXT,
    speaker TEXT,
    transcript TEXT
);

-- Activity log
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY,
    agent_type TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
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

### Docker Compose

```yaml
version: '3.8'
services:
  mediaagentiq:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    environment:
      - PRODUCTION_MODE=true
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
```

### Production Recommendations

1. **Reverse Proxy:** Nginx/Caddy for HTTPS
2. **Database:** PostgreSQL for production
3. **Cache:** Redis for session/task caching
4. **Queue:** Redis/RabbitMQ for task queue
5. **Monitoring:** Prometheus + Grafana
6. **Logging:** ELK Stack or CloudWatch

---

## 📈 Changelog

### v2.0.0 (Latest)
- ✅ Autonomous Agent Orchestrator
- ✅ All-in-One Workflow
- ✅ Integration Showcase
- ✅ Real-time processing indicators
- ✅ Dual-mode architecture
- ✅ Service layer (Whisper, Vision, Dubbing)
- ✅ MAM integration (Avid)
- ✅ NMOS integration (IS-04/IS-05)
- ✅ Enhanced Streamlit UI (2400+ lines)

### v1.0.0
- Initial release
- 8 AI agents (demo mode)
- FastAPI backend
- Basic Streamlit UI

---

## 📝 License

MIT License - Built for Media & Broadcast professionals

---

**MediaAgentIQ v2.0.0** | Enterprise AI Platform for Media Operations

*Last Updated: February 2026*
