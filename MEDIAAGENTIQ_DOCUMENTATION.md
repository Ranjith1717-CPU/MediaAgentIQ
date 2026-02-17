# MediaAgentIQ - AI Agent Platform for Media & Broadcast

## 📋 Overview

MediaAgentIQ is an AI-powered agent platform designed specifically for media and broadcast organizations. It provides 8 specialized AI agents that automate critical workflows, from captioning to compliance monitoring, viral clip detection to rights management.

**Inspired by:** Buzzboard's SMB model, adapted for enterprise media/broadcast clients.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Windows/Mac/Linux

### Installation

```bash
# Navigate to project directory
cd "C:\Users\ranjith\Desktop\AI Kalari\MediaAgentIQ"

# Option 1: Use the Windows batch launcher
run.bat

# Option 2: Manual setup
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Access Dashboard
Open your browser: **http://localhost:8000**

---

## 🤖 The 8 AI Agents

### 1. 📝 Caption Agent
**Purpose:** Auto-generate captions with QA checks

**Features:**
- AI-powered speech-to-text transcription
- Speaker detection and labeling
- Timing optimization for perfect sync
- Automated QA checks (confidence scores, profanity detection, timing gaps)
- Multi-format export (SRT, VTT)

**API Endpoint:** `POST /api/caption/process`

**Input:** Video/audio file upload (MP4, MOV, AVI, MKV, WebM, MP3, WAV, M4A)

**Output:**
```json
{
  "success": true,
  "data": {
    "captions": [...],
    "qa_results": [...],
    "srt": "SRT content",
    "vtt": "VTT content",
    "stats": {
      "total_segments": 11,
      "word_count": 95,
      "qa_issues": 2
    }
  }
}
```

**Value Proposition:** 80% reduction in captioning costs

---

### 2. 🎬 Clip Agent
**Purpose:** Monitor broadcasts, identify viral moments, auto-create social clips

**Features:**
- Real-time viral moment detection
- Emotional peak analysis
- Engagement score prediction
- Multi-platform optimization (TikTok, Reels, Shorts, Twitter)
- Auto-generated hashtags
- Social post suggestions

**API Endpoint:** `POST /api/clip/process`

**Input:** Video file upload

**Output:**
```json
{
  "viral_moments": [...],
  "suggested_clips": [
    {
      "id": "clip_1234",
      "start": 45.5,
      "end": 60.0,
      "viral_score": 0.95,
      "emotion": "excitement",
      "hashtags": ["#Breaking", "#Viral"]
    }
  ],
  "social_posts": [...]
}
```

**Value Proposition:** 10x more social content, zero editing time

---

### 3. 🔍 Archive Agent
**Purpose:** Natural language search for archived content

**Features:**
- Natural language query parsing
- Date/time period extraction
- Speaker/person detection
- Topic analysis
- Relevance scoring
- Search insights and suggestions

**API Endpoint:** `POST /api/archive/search`

**Input:**
```json
{
  "query": "Find all Biden economy clips from Q3",
  "filters": {}
}
```

**Output:**
```json
{
  "query": "Find all Biden economy clips from Q3",
  "parsed_query": {
    "topics": ["economy"],
    "speakers": ["Biden"],
    "date_filters": {"time_period": "Q3"}
  },
  "results": [...],
  "insights": {
    "summary": "Found 15 clips totaling 2:30:00",
    "top_tags": ["economy", "politics"]
  }
}
```

**Value Proposition:** Instant archive access (vs. hours of manual searching)

---

### 4. ⚖️ Compliance Agent
**Purpose:** 24/7 FCC violation monitoring

**Features:**
- Profanity/indecency detection (FCC § 326)
- Political ad disclosure checking (FCC § 315)
- Sponsor identification verification (FCC § 317)
- Caption quality compliance (47 CFR § 79.1)
- Emergency Alert System compliance
- Risk scoring and fine estimation

**API Endpoint:** `POST /api/compliance/scan`

**Input:** Video/audio file or transcript text

**Output:**
```json
{
  "issues": [
    {
      "type": "profanity",
      "severity": "high",
      "timestamp": "00:02:05,500",
      "fcc_rule": "47 U.S.C. § 326",
      "potential_fine": "$25,000 - $500,000",
      "recommendation": "Review segment, consider bleeping"
    }
  ],
  "risk_score": {"score": 65, "level": "medium"},
  "stats": {
    "total_issues": 4,
    "potential_fines": "$35,000 - $550,000"
  }
}
```

**Value Proposition:** Avoid $500K+ FCC fines

---

### 5. 📱 Social Publishing Agent
**Purpose:** Create and schedule social posts from broadcast content

**Features:**
- Multi-platform post generation (Twitter/X, Instagram, TikTok, Facebook, YouTube Shorts)
- Platform-specific formatting
- Optimal posting time scheduling
- Hashtag recommendations
- Performance predictions
- Engagement rate estimation

**API Endpoint:** `POST /api/social/generate`

**Input:**
```json
{
  "content": "highlight content or clip reference"
}
```

**Output:**
```json
{
  "posts": [
    {
      "platform": "twitter",
      "content": "🔴 BREAKING: Major Development...",
      "char_count": 180,
      "best_time": "9:00 AM EST"
    }
  ],
  "schedule": [...],
  "hashtags": {
    "trending": ["#Breaking", "#Viral"],
    "niche": ["#BroadcastNews"]
  },
  "predictions": [
    {
      "predicted_reach": "50K",
      "predicted_engagement": "5.2%"
    }
  ]
}
```

**Value Proposition:** Always-on social presence

---

### 6. 🌍 Localization Agent
**Purpose:** Auto-translate captions and generate dubs

**Features:**
- Support for 12+ languages (Spanish, French, German, Chinese, Japanese, etc.)
- AI translation with confidence scoring
- Quality assessment (fluency, accuracy, cultural adaptation)
- AI dubbing with voice selection
- Lip-sync technology support
- Multi-language workflow management

**API Endpoint:** `POST /api/localization/translate`

**Input:**
```json
{
  "content": "caption content",
  "target_languages": ["es", "fr", "de", "zh"]
}
```

**Output:**
```json
{
  "translations": {
    "es": {
      "language_name": "Spanish",
      "segments": [...],
      "srt_content": "...",
      "vtt_content": "..."
    }
  },
  "dub_options": [...],
  "workflow": {
    "steps": [...],
    "overall_progress": 14
  },
  "quality_report": {
    "language_scores": {
      "es": {"overall_score": 94.5, "fluency": 96}
    }
  }
}
```

**Value Proposition:** Faster global distribution

---

### 7. 📜 Rights Agent
**Purpose:** Track content licenses and monitor unauthorized usage

**Features:**
- License tracking and management
- Expiry alerts (90/60/30 day warnings)
- Unauthorized usage detection
- DMCA takedown workflow
- Territorial violation monitoring
- Cost and damages tracking

**API Endpoint:** `POST /api/rights/check`

**Output:**
```json
{
  "licenses": [
    {
      "id": "LIC001",
      "content_title": "Premier League Highlights",
      "license_type": "time_limited",
      "end_date": "2024-12-31",
      "cost": "$500,000/year",
      "rights": ["broadcast", "streaming"]
    }
  ],
  "expiring_soon": [...],
  "violations": [
    {
      "type": "unauthorized_rebroadcast",
      "detected_on": "YouTube",
      "estimated_damages": "$25,000"
    }
  ],
  "alerts": [...]
}
```

**Value Proposition:** Avoid legal disputes

---

### 8. 📈 Trending Agent
**Purpose:** Monitor trends and alert newsroom to breaking stories

**Features:**
- Real-time social media monitoring (Twitter/X, TikTok, Reddit, etc.)
- News wire integration (AP, Reuters, AFP, Bloomberg)
- Trend velocity analysis
- Sentiment analysis
- Viral content detection
- Newsroom alert generation
- Story suggestions with coverage angles

**API Endpoint:** `POST /api/trending/monitor`

**Input:**
```json
{
  "filters": {"category": "technology"}
}
```

**Output:**
```json
{
  "trends": [
    {
      "topic": "AI Regulation Debate",
      "velocity": "rising",
      "velocity_score": 78,
      "volume": "180K mentions/hour",
      "sentiment": "mixed"
    }
  ],
  "breaking_news": [...],
  "viral_content": [...],
  "alerts": [
    {
      "type": "breaking_news",
      "priority": "high",
      "title": "BREAKING: Major Economic Announcement"
    }
  ],
  "story_suggestions": [...]
}
```

**Value Proposition:** Never miss a story

---

## 📁 Project Structure

```
MediaAgentIQ/
├── app.py                      # FastAPI main application (routes & endpoints)
├── config.py                   # Configuration settings
├── database.py                 # SQLite database setup & operations
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows launcher script
│
├── agents/                     # AI Agent implementations
│   ├── __init__.py            # Agent exports & registry
│   ├── base_agent.py          # Base agent class (abstract)
│   ├── caption_agent.py       # Caption generation & QA
│   ├── clip_agent.py          # Viral clip detection
│   ├── archive_agent.py       # Content search & retrieval
│   ├── compliance_agent.py    # FCC compliance monitoring
│   ├── social_publishing_agent.py  # Social media post generation
│   ├── localization_agent.py  # Translation & dubbing
│   ├── rights_agent.py        # License & rights management
│   └── trending_agent.py      # Trend monitoring & alerts
│
├── templates/                  # Jinja2 HTML templates
│   ├── index.html             # Dashboard home page
│   ├── caption.html           # Caption Agent UI
│   ├── clip.html              # Clip Agent UI
│   ├── archive.html           # Archive Agent UI
│   ├── compliance.html        # Compliance Agent UI
│   ├── social.html            # Social Publishing Agent UI
│   ├── localization.html      # Localization Agent UI
│   ├── rights.html            # Rights Agent UI
│   └── trending.html          # Trending Agent UI
│
├── static/
│   ├── css/
│   │   └── styles.css         # Custom CSS styles
│   └── js/
│       └── app.js             # Frontend JavaScript
│
├── uploads/                    # Uploaded media files (auto-created)
├── outputs/                    # Generated outputs (auto-created)
└── demo_data/                  # Sample data for demos (auto-created)
```

---

## 🗄️ Database Schema

SQLite database (`mediaagentiq.db`) with these tables:

### jobs
Tracks all agent processing jobs
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    agent_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    input_file TEXT,
    output_file TEXT,
    result_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);
```

### archive
Mock video archive for search
```sql
CREATE TABLE archive (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    duration INTEGER,
    date_recorded DATE,
    tags TEXT,
    speaker TEXT,
    transcript TEXT,
    thumbnail_url TEXT,
    video_url TEXT
);
```

### compliance_issues
Compliance violations found
```sql
CREATE TABLE compliance_issues (
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    issue_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    timestamp_start REAL,
    timestamp_end REAL,
    description TEXT,
    suggestion TEXT
);
```

### activity_log
Recent activity tracking
```sql
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY,
    agent_type TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.9+, FastAPI |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript |
| **Database** | SQLite (aiosqlite for async) |
| **AI** | OpenAI API (optional) or mock responses |
| **Server** | Uvicorn ASGI server |
| **Templates** | Jinja2 |

### Dependencies (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
jinja2==3.1.2
aiosqlite==0.19.0
openai==1.3.5
python-dotenv==1.0.0
aiofiles==23.2.1
```

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard home |
| GET | `/caption` | Caption Agent UI |
| POST | `/api/caption/process` | Process media for captions |
| GET | `/clip` | Clip Agent UI |
| POST | `/api/clip/process` | Find viral clips |
| GET | `/archive` | Archive Agent UI |
| POST | `/api/archive/search` | Search archive |
| GET | `/compliance` | Compliance Agent UI |
| POST | `/api/compliance/scan` | Run compliance scan |
| GET | `/social` | Social Publishing Agent UI |
| POST | `/api/social/generate` | Generate social posts |
| GET | `/localization` | Localization Agent UI |
| POST | `/api/localization/translate` | Translate content |
| GET | `/rights` | Rights Agent UI |
| POST | `/api/rights/check` | Check licenses/rights |
| GET | `/trending` | Trending Agent UI |
| POST | `/api/trending/monitor` | Monitor trends |
| GET | `/api/stats` | Get dashboard stats |
| GET | `/api/activity` | Get recent activity |
| GET | `/download/{filename}` | Download generated file |

---

## 🎨 UI/UX Design

### Color Scheme
- **Background:** Slate-950 (#020617)
- **Cards:** Slate-900 (#0f172a)
- **Borders:** Slate-800 (#1e293b)
- **Primary:** Indigo-500 (#6366f1)
- **Secondary:** Purple-500 (#a855f7)

### Agent Colors
| Agent | Color |
|-------|-------|
| Clip | Purple |
| Caption | Blue |
| Compliance | Red |
| Archive | Green |
| Social | Pink |
| Localization | Cyan |
| Rights | Orange |
| Trending | Yellow |

---

## 🔧 Configuration

### config.py Options

```python
# File paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

# Database
DATABASE_PATH = BASE_DIR / "mediaagentiq.db"

# OpenAI (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_MOCK_AI = not OPENAI_API_KEY  # Uses mock if no key

# Server
HOST = "127.0.0.1"
PORT = 8000
DEBUG = True

# Upload limits
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac"}
```

### Environment Variables
```bash
# Optional: Set OpenAI API key for real AI processing
export OPENAI_API_KEY="sk-..."
```

---

## 🧪 Testing the Demo

### 1. Caption Agent
1. Go to http://localhost:8000/caption
2. Upload any video/audio file
3. View generated captions and QA report
4. Download SRT/VTT files

### 2. Clip Agent
1. Go to http://localhost:8000/clip
2. Upload a video file
3. View detected viral moments with scores
4. See suggested social posts

### 3. Archive Agent
1. Go to http://localhost:8000/archive
2. Type natural language query: "Find election coverage"
3. View matching results with relevance scores

### 4. Compliance Agent
1. Go to http://localhost:8000/compliance
2. Click "Run Compliance Scan" (uses demo content)
3. View detected issues, risk score, and recommendations

### 5. Social Publishing Agent
1. Go to http://localhost:8000/social
2. Click "Generate Social Posts"
3. View posts for Twitter, Instagram, TikTok
4. Copy posts or schedule them

### 6. Localization Agent
1. Go to http://localhost:8000/localization
2. Select target languages
3. Click "Start Localization"
4. View translations and quality scores

### 7. Rights Agent
1. Go to http://localhost:8000/rights
2. Click "Check All Licenses & Rights"
3. View licenses, expiring alerts, violations

### 8. Trending Agent
1. Go to http://localhost:8000/trending
2. Auto-loads trending topics on page load
3. Filter by category
4. View newsroom alerts and story suggestions

---

## 🚀 Production Deployment

### Recommended Setup
1. Use production ASGI server (Gunicorn + Uvicorn workers)
2. Set up PostgreSQL instead of SQLite
3. Use Redis for caching
4. Deploy behind Nginx/Caddy reverse proxy
5. Enable HTTPS
6. Set proper CORS headers
7. Add authentication (OAuth2/JWT)

### Docker Deployment (Example)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📈 Future Enhancements

### Phase 2 Features
- [ ] Real OpenAI Whisper integration for transcription
- [ ] Actual video processing with FFmpeg
- [ ] User authentication & multi-tenancy
- [ ] Real-time WebSocket updates
- [ ] Email/Slack notifications
- [ ] API rate limiting
- [ ] Batch processing queue
- [ ] Analytics dashboard

### Phase 3 Features
- [ ] Custom model fine-tuning
- [ ] Live broadcast monitoring
- [ ] Automated publishing to social platforms
- [ ] Integration with MAM systems
- [ ] Mobile app companion

---

## 📞 Support & Contact

**Project Location:** `C:\Users\ranjith\Desktop\AI Kalari\MediaAgentIQ`

**Created:** February 2026

**Version:** 1.0.0

---

## 📝 License

This is a prototype/demo project for AI Kalari.

---

*MediaAgentIQ - AI-Powered Media Operations Platform*
