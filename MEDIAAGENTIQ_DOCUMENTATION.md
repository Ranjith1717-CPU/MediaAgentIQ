# MediaAgentIQ v3.3 — Complete Documentation

## 📋 Overview

MediaAgentIQ is an enterprise AI-powered agent platform for media and broadcast organizations. It provides **19 specialized AI agents** that run **autonomously 24/7** across the full broadcast pipeline, with persistent memory and standing-instruction rules — and are reachable directly from **Slack and Microsoft Teams**.

**Key Features:**
- 🤖 **Autonomous Operation** — 19 agents, 14 scheduled jobs, event-driven chains
- 🔮 **HOPE Engine** — Standing-instruction layer. Tell an agent something once from Slack and it acts autonomously every time, forever, until you cancel
- 🧠 **Persistent Agent Memory** — Every agent maintains a `.md` log of past decisions, inputs, outputs, and triggered events. Memory is injected into LLM prompts for context-aware operation
- 🔄 **Dual-Mode Architecture** — Demo mode (no API keys) + Production mode (real AI)
- 💬 **Slack & Teams Integration** — Trigger any agent from your workspace via `/miq-*` slash commands or natural language
- 🔌 **MCP Connector Framework** — Plugin architecture. Any external system exposed as a tool agents can discover and call
- 🚀 **All-in-One Workflow** — Process content through all 19 agents simultaneously
- 🛡️ **Future-Ready** — 6 market-gap agents solving problems no broadcast vendor has tackled

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
  Inter-Agent Event Logger → inter_agent_comms.md
  System State Snapshots  → system_state.md (every 300s)
         │
Agent Layer (19 agents)   [agents/]
  Original 8 + Future-Ready 6 + Phase 1 Pipeline 5
  BaseAgent: timing + memory save + HOPE eval on every process() call
         │
HOPE Engine   [memory/hope_engine.py]    ← NEW v3.3
  HopeRule dataclass (condition, schedule, priority, status)
  HopeEngine per agent: add/cancel/list/evaluate/fire rules
  HOPE.md + companion files auto-created per agent
  Mute hours (23:00–07:00) • Rate limit (10 alerts/hour)
  CRITICAL priority bypasses all guards
  UserProfile → Slack channel routing by priority
         │
Persistent Agent Memory Layer   [memory/]    ← v3.2
  AgentMemoryLayer (one instance per agent)
  memory/agents/{slug}/HOPE.md       → standing rules
  memory/agents/{slug}/MEMORY.md     → task log
  memory/agents/inter_agent_comms.md → cross-agent event log
  memory/agents/task_history.md      → global audit table
  memory/agents/system_state.md      → orchestrator snapshot
  get_memory_context_prompt()        → LLM system-prompt injection
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

Every agent supports two modes, with automatic timing, memory persistence, and HOPE evaluation on every call:
```python
class BaseAgent:
    async def process(self, input_data):
        _start = time.monotonic()
        await self.validate_input(input_data)
        if self.is_production_mode:
            result = await self._production_process(input_data)  # Real AI/APIs
        else:
            result = await self._demo_process(input_data)         # Realistic mock data
        # Automatically saves to memory/agents/{slug}/MEMORY.md
        self._save_to_memory(input_data, result, duration_ms, triggered_events=[])
        # HOPE evaluation — non-fatal; fires Slack alerts for matching standing rules
        if self._hope:
            matched = self._hope.evaluate(result)
            for rule in matched:
                self._hope.fire_action(rule, result, notifier=self._get_notifier())
        return result

    def get_memory_context_prompt(self) -> str:
        """Return last N task entries as a formatted LLM system-prompt block."""
        return self._memory.get_memory_context_prompt()

    # HOPE management (called by gateway)
    def add_hope_rule(self, condition, schedule, action, priority) -> dict: ...
    def cancel_hope_rule(self, rule_id) -> dict: ...
    def list_hope_rules(self) -> list: ...
```

### HOPE Engine (NEW v3.3)

`HopeEngine` is instantiated per agent during `__init__` when `HOPE_ENABLED=True`. It stores standing rules in `memory/agents/{slug}/HOPE.md` and evaluates them on every `process()` call.

**HOPE.md format:**
```markdown
# archive_agent — HOPE Rules
_Last updated: 2026-02-28 14:23:01 | Active rules: 2 | Total fired: 47_

---

## hope_001 [ACTIVE]
**Condition**: Trump speaking to press
**Schedule**: DAILY 08:00 IST
**Action**: Send Slack DM to @ranjith with clip link and summary
**Priority**: HIGH
**Created**: 2026-02-28 09:00:00
**Trigger count**: 12
**Last triggered**: 2026-02-28 08:01:03
```

**Key methods:**

| Method | Purpose |
|--------|---------|
| `load()` | Create `HOPE.md` + 5 companion files if missing |
| `add_rule(condition, schedule, action, priority)` | Append new ACTIVE rule; return `HopeRule` |
| `cancel_rule(rule_id)` | Set status=INACTIVE in file |
| `list_rules()` | Parse all rules from HOPE.md |
| `evaluate(result)` | Check ACTIVE IMMEDIATE rules against result; return matched list |
| `fire_action(rule, result, notifier)` | Increment count, update timestamp, send Slack alert |
| `get_daily_digest_rules()` | Return ACTIVE DAILY-schedule rules |
| `run_daily_digests(results, notifier)` | Bundle results since midnight; send digest per rule |

**Alert routing:**

| Priority | Schedule | Muted (23–07)? | Channel |
|----------|----------|----------------|---------|
| CRITICAL | IMMEDIATE | No (bypasses) | Slack DM + @here in #breaking-alerts |
| HIGH | IMMEDIATE | Yes | Slack DM only |
| NORMAL | IMMEDIATE | Yes | #media-alerts |
| LOW | DAILY | N/A | 08:00 digest only |

**Companion files** (auto-created per agent):
```
memory/agents/{slug}/
  HOPE.md       ← standing rules
  AGENTS.md     ← relationships to other agents
  MEMORY.md     ← recent task summaries
  SOUL.md       ← agent personality + priorities
  TOOLS.md      ← available tools + integrations
  IDENTITY.md   ← agent metadata
  logs/         ← daily log files (YYYY-MM-DD.md)
```

**HOPE natural language examples (Slack):**
```
"whenever you detect Trump speaking, alert me immediately"
"every morning send me a digest of breaking war news"
"alert me if brand safety drops below 70"
"stop watching hope_001"
"list my rules for archive agent"
```

---

### Memory Layer

`AgentMemoryLayer` is instantiated for every agent during `__init__` when `MEMORY_ENABLED=True`. It writes to plain `.md` files — human-readable, version-controllable, and zero-dependency.

#### Why Plain Markdown Files?

The choice of `.md` files over a database is deliberate and has significant advantages:

1. **Human readability** — An engineer can `cat memory/agents/caption_agent/MEMORY.md` and immediately understand what the agent has been doing. No query language, no schema to learn.
2. **Git native** — Memory files are version-controlled alongside code. A git diff shows exactly how an agent's knowledge has changed between deployments.
3. **LLM native** — Markdown is the format LLMs reason about best. Injecting a `.md` block into a system prompt is semantically richer than injecting JSON rows.
4. **Zero dependency** — The memory layer works with no database, no cache server, no external services. It starts on any machine that has a filesystem.
5. **Inspectable during incidents** — When something goes wrong at 03:00, an engineer can read what the agent was doing in the last 48 hours by opening a single file in a text editor.

The trade-off is that plain files do not scale to millions of rows without management. The trim system, archive rotation, and distillation pipeline address this at each growth stage.

**Per-agent file** (`memory/agents/caption_agent.md`):
```markdown
# Caption Agent — Memory Log
_Last updated: 2026-02-28 14:23:01 | Entries: 47 | Success rate: 96.8% | Avg duration: 312ms_

---

## [2026-02-28 14:23:01] Task `a3f7c1` SUCCESS (demo)
**Input**: `news_segment_04.mp4`
**Output**: segments=11, qa_issues=1, confidence_avg=0.97
**Triggered**: caption_complete → localization_agent, social_publishing_agent, live_fact_check_agent
**Duration**: 234ms
```

**Inter-agent event log** (`memory/agents/inter_agent_comms.md`):
```markdown
## [2026-02-28 14:23:01] CAPTION_COMPLETE
**Source**: caption (task `a3f7c1`)
**Subscribers**: localization, social, live_fact_check
**Payload summary**: captions=1, data={...}
**Tasks queued**: 3
```

**Key methods:**

| Method | Returns | Notes |
|--------|---------|-------|
| `load()` | — | Creates file if missing, warms context cache |
| `save_task(task_id, input, result, duration_ms, triggered)` | — | Appends entry, trims, updates header |
| `update_last_entry_triggered(triggered)` | — | Patches last entry after events fire |
| `log_inter_agent_event(...)` | — | Appends to shared `inter_agent_comms.md` |
| `get_agent_stats()` | `dict` | O(1) parse of header line: entries/success/avg |
| `get_memory_context_prompt()` | `str` | Last N entries for LLM injection |

#### Memory Growth at Scale — Full Lifecycle

Understanding how memory grows — and what controls are in place at each stage — is important for production deployments running for months or years.

**Current safeguards (v3.2+):**

```bash
MEMORY_MAX_ENTRIES_PER_AGENT=500    # When any agent's file exceeds this, trim runs
MEMORY_TRIM_TO=400                  # Oldest 100 entries removed, newest 400 kept
MEMORY_INTER_AGENT_MAX_ENTRIES=2000 # inter_agent_comms.md hard cap
MEMORY_TASK_HISTORY_MAX_ENTRIES=5000# task_history.md hard cap (global audit)
MEMORY_RECENT_CONTEXT_ENTRIES=5     # Only last 5 entries injected into LLM prompts
```

With these defaults, the system reaches a steady-state footprint:

| File | Steady-state size | Notes |
|------|-------------------|-------|
| Per-agent `MEMORY.md` | ~80KB | Trim keeps it bounded indefinitely |
| `task_history.md` | ~500KB | 5,000 rows × ~100 bytes each |
| `inter_agent_comms.md` | ~200KB | 2,000 entries × ~100 bytes each |
| `system_state.md` | ~10KB | Fully rewritten every 300s; never grows |
| Per-agent daily `logs/YYYY-MM-DD.md` | ~5KB/day per agent | These grow without bound — archive or prune monthly |
| **Total (19 agents, no archiving)** | **~2–4MB** | Manageable indefinitely on any filesystem |

**What "grows without bound" if left unmanaged:**

The daily log files in `memory/agents/{slug}/logs/` are currently **not trimmed**. At 5KB/day/agent × 19 agents, that is ~35KB/day, or ~1GB over 80 years — not a practical concern. But in a high-throughput production environment (many events per minute), individual daily log files could reach 1–5MB, making the `logs/` directory grow at 10–100MB/month per busy agent. The mitigation is the monthly archive rotation in the roadmap (compress logs older than 30 days to `.md.gz`).

#### The Three-Tier Memory Architecture (Roadmap)

As the platform runs beyond 6–12 months, the memory strategy evolves from "trim and discard old" to "preserve and make searchable":

```
┌──────────────────────────────────────────────────────────────────┐
│  TIER 1 — Hot Memory (current .md files, always available)        │
│                                                                    │
│  What: Last 400–500 task entries per agent                        │
│  Where: memory/agents/{slug}/MEMORY.md                            │
│  Size: ~80KB per agent (bounded by trim)                          │
│  Access: Synchronous file read — <1ms                             │
│  LLM use: Last 5 entries injected into every system prompt        │
│  Retention: Rolling — oldest entries removed when cap hit         │
└──────────────────────────────────────────────────────────────────┘
           ↓ entries "age out" via trim
┌──────────────────────────────────────────────────────────────────┐
│  TIER 2 — Warm Memory (structured DB, queryable)                  │
│                                                                    │
│  What: All tasks from last 6 months, structured rows              │
│  Where: SQLite (dev) / PostgreSQL (production)                    │
│  Size: ~500KB–50MB depending on event volume                      │
│  Access: SQL query — ~5–50ms                                      │
│  LLM use: Retrieved on demand ("what happened last month?")       │
│  Retention: 6-month rolling window, then archive to Tier 3        │
│  Schema: (agent, task_id, ts, success, duration_ms, tags, summary)│
└──────────────────────────────────────────────────────────────────┘
           ↓ rows "age out" after 6 months
┌──────────────────────────────────────────────────────────────────┐
│  TIER 3 — Cold Memory (archive, retrievable on demand)            │
│                                                                    │
│  What: All tasks older than 6 months                              │
│  Where: S3 / local archive as YYYY-MM.md.gz per agent per month   │
│  Size: Grows indefinitely; 1–10MB compressed per agent per month  │
│  Access: Explicit recall via /miq-recall command or HOPE rule     │
│  LLM use: Decompressed and injected only when explicitly recalled │
│  Retention: Permanent (regulatory and ESG reporting requirements) │
└──────────────────────────────────────────────────────────────────┘
```

#### Memory Distillation — Preserving Institutional Knowledge

The most important long-term capability is **memory distillation**: periodically using an LLM to compress hundreds of raw task entries into compact, high-signal summaries stored in `SOUL.md`.

Raw task logs capture *what happened*. Distilled memory captures *what it means* — patterns, failure modes, edge cases, and learned behaviours that make the agent genuinely smarter over time, not merely larger in storage.

**Distillation process (Sunday 03:00 UTC, weekly):**

```
1. Read last 500 entries from {agent}/MEMORY.md
2. Send to LLM with prompt:
   "You are reviewing one week of autonomous broadcast AI agent activity.
    Summarise the key operational patterns, recurring failure modes,
    notable edge cases, and learned behaviours from these 500 tasks.
    Output ≤10 bullet points that will help the agent make better
    decisions next week. Be specific to broadcast operations."
3. Append distilled summary to {agent}/SOUL.md:
   ## Institutional Memory — [week of YYYY-MM-DD]
   - [bullet point 1]
   - [bullet point 2]
   ...
4. Archive raw 500 entries to Tier 2 / Tier 3
5. The agent's next LLM prompt will include:
   - SOUL.md (distilled wisdom from all prior weeks)
   - Last 5 hot entries from MEMORY.md (this week's context)
   Combined: maximum signal, minimum noise
```

**What distilled SOUL.md looks like after 6 months of operation:**

```markdown
# Caption Agent — SOUL

## Operational Identity
Broadcast-grade caption generation for live and VOD content.
Accuracy target: 98%+ on studio audio, 94%+ on location audio.

## Institutional Memory — week of 2026-02-23
- QA failure rate increased 8% for segments >45 minutes — likely drift in
  confidence scoring for long-form content. Flag for threshold review.
- Location audio from the Westminster studio exhibits consistent -3dB
  headroom issue; Whisper confidence drops to 0.84 on that feed.
- Emergency news segments processed 22% faster when pre-segmented at
  sentence breaks rather than fixed 10-second intervals.

## Institutional Memory — week of 2026-02-16
- Breaking news segments with >3 speakers showed 12% higher caption
  error rate. Diarization model upgrade needed.
- 100% of overnight auto-caption runs succeeded — overnight processing
  window is the most reliable; consider scheduling large batches then.

## Institutional Memory — week of 2026-01-05
- Election night: 847 segments processed in 6 hours. Throughput ceiling
  identified at ~140 segments/hour on single node. Scale trigger: 100/hr.
```

This is how a broadcast organisation builds **AI institutional memory** — structured, compressed, LLM-injectable knowledge that persists across deployments, model upgrades, and staff changes. An agent with 12 months of distilled SOUL.md has a deeper understanding of a specific broadcast operation's quirks than any new-hire operator.

#### Memory as Competitive Moat

An agent platform installed and running continuously for 12 months has accumulated:

- Every compliance edge case that network's content has triggered
- Every brand safety override decision and the editorial reasoning behind it
- Every deepfake false positive and the audio/video patterns that caused it
- Every breaking-news rundown reshuffling decision the Production Director made
- Every signal quality anomaly and how the NOC responded

This is **not replaceable** by a competitor installing a fresh agent platform. It is the distilled operational intelligence of the broadcast organisation, held by agents that understand that organisation's specific workflows, audiences, standards, and failure modes.

This is why persistent memory is not a feature — it is the long-term strategic moat of the platform.

---

## 🌐 The Future of Slack-Native AI Agents

### Why Slack and Teams are Becoming the Primary AI Interface

The most significant UX shift in enterprise software since the move to web browsers is happening right now: the **death of the dedicated dashboard**. In 2024–2026, every major enterprise AI initiative is converging on a single insight — the best place to put an AI agent is inside the tool where the user already spends their day.

For broadcast operations, that tool is Slack (or Teams at legacy-IT-heavy organisations). When a compliance producer can type `/miq-compliance rtmp://live/channel1` and get a scored result with action buttons in under five seconds, without switching applications, the adoption friction drops to near zero. The agent becomes as natural as sending a message.

This is the precise pattern that has made the following products successful at enterprise scale in 2025–2026:

**Communication-embedded AI agents (2025–2026):**
- **Microsoft 365 Copilot** — agents answering questions in Teams threads, drafting documents on mention, attending meetings and summarising action items
- **Salesforce Agentforce** — autonomous CRM agents operating inside Slack, taking actions on Salesforce objects in response to natural language
- **Atlassian Rovo** — agents with cross-workspace knowledge of Jira, Confluence, and git history, surfaced in Slack via mentions
- **Workday AI** — HR agents answering benefits, leave, and payslip questions inside Teams, reducing HR ticket volume by 40%+
- **Zendesk AI** — support agents resolving 60%+ of tickets autonomously via Slack-connected channels

The common thread: **agents that live where the work is done, not in a separate portal**.

### The Paradigm Shift in Agent Interaction Models

Traditional software requires users to navigate to the tool. Agent-native software inverts this relationship — the intelligence comes to the user, in context, when they need it.

```
Traditional model:
  User notices a problem → opens browser → navigates to dashboard →
  logs in → finds the right page → interprets the metric →
  decides an action → manually executes it → goes back to Slack

Agent-native model:
  Agent detects the problem → sends Slack alert with context →
  user reads one card → clicks one button → done
```

For broadcast operations, this difference is measured in **minutes that matter during live transmission**. A compliance alert that arrives in the NOC's Slack channel with an auto-correct button is actionable in 10 seconds. The same alert sitting in a monitoring dashboard that nobody has open is actionable in however long it takes someone to notice it — which in broadcast could be after the segment has aired.

### The HOPE Engine in Global Context

Standing instructions — "whenever X happens, do Y, indefinitely, until I say stop" — are emerging as a first-class primitive in production AI systems worldwide:

| Platform | Standing Instruction Pattern |
|----------|------------------------------|
| Claude Code `CLAUDE.md` | Persistent behavioural rules injected into every session |
| OpenAI Assistants `instructions` | System prompt that persists across all threads |
| LangGraph checkpointing | Agent state (including rules) persisted to database between runs |
| Zapier AI | "Zaps" as standing if-this-then-that rules for AI actions |
| Make.com / n8n agents | Trigger-based rules that fire autonomous AI workflows |
| PagerDuty AI | Alert routing rules that learn from human overrides |

MediaAgentIQ's HOPE Engine is the broadcast-domain realisation of this pattern. Where Claude Code's CLAUDE.md shapes how an AI assistant codes, HOPE.md shapes how a compliance agent monitors a live feed — autonomously, persistently, with human-specified conditions.

The naming is deliberate: HOPE rules express what you *hope* the agent will watch for on your behalf. They are the standing contracts between broadcast operators and their AI colleagues.

### Industry Analysts on Agent-Native Broadcast

The broadcast and media technology sector is the **last major enterprise vertical** to undergo AI transformation, trailing finance (algorithmic trading agents, compliance AI since 2018), healthcare (clinical decision support agents since 2020), and e-commerce (recommendation and fraud detection agents since 2016) by significant margins.

Key analyst data points (2025–2026):

- **Gartner Hype Cycle for Media Technology (2025):** Agentic AI for media production listed as a "Peak of Inflated Expectations" technology, predicted to reach "Plateau of Productivity" by 2027–2028. First movers in this window will define the category.
- **IBC Show Report (2025):** Only 3% of broadcasters surveyed had deployed autonomous AI agents in their production workflow. 78% said they planned to evaluate vendor options in 2026–2027.
- **Omdia Broadcast AI Report (2025):** The primary barrier to AI adoption in broadcast is not capability but **workflow integration** — operators won't use tools that require leaving their existing interfaces. Slack/Teams integration is identified as the key enabler.
- **NAB Show 2025 Trend Summary:** The most-discussed infrastructure theme was "AI agents inside existing broadcast workflows, not alongside them." No incumbent vendor demonstrated a live, Slack-connected AI agent platform.

MediaAgentIQ's positioning — 19 agents, fully Slack/Teams native, with standing-instruction capabilities and persistent memory — is precisely what analysts describe as the target state for the category. It is currently being built by a startup, not by the incumbents.

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
3. **HOPE intent detection** — intercepts standing-instruction phrases (`whenever`, `alert me if`, `stop watching`, `list my rules`); returns `__hope_create__` / `__hope_cancel__` / `__hope_list__`
4. **Claude LLM fallback** — for ambiguous or complex requests (requires `OPENAI_API_KEY`)

### Slash Commands Reference

| Command | Agent | Example |
|---------|-------|---------|
| `/miq-hope` | HOPE Engine | Create a standing rule (interactive) |
| `/miq-hope-list` | HOPE Engine | List all active rules |
| `/miq-hope-cancel hope_001` | HOPE Engine | Cancel rule by ID |
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

# ─── Memory Layer ─────────────────────────────────────────
MEMORY_ENABLED=true                        # Disable to turn off all .md logging
MEMORY_DIR=memory                          # Root directory (relative to project)
MEMORY_MAX_ENTRIES_PER_AGENT=500           # Trim trigger per agent file
MEMORY_TRIM_TO=400                         # Entries kept after trim
MEMORY_RECENT_CONTEXT_ENTRIES=5            # Entries injected into LLM prompts
MEMORY_INTER_AGENT_MAX_ENTRIES=2000        # Max entries in inter_agent_comms.md
MEMORY_TASK_HISTORY_MAX_ENTRIES=5000       # Max rows in task_history.md
MEMORY_SYSTEM_STATE_INTERVAL_SECS=300      # system_state.md rewrite interval

# ─── HOPE Engine ──────────────────────────────────────────
HOPE_ENABLED=true                          # Disable to turn off standing-instruction engine
HOPE_MAX_ALERTS_PER_HOUR=10               # Rate-limit non-critical alerts per agent per hour
HOPE_MUTE_START_HOUR=23                   # Start of quiet hours (local time, 24h clock)
HOPE_MUTE_END_HOUR=7                      # End of quiet hours (CRITICAL bypasses mute)

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
├── settings.py                    # Pydantic config (70+ typed settings incl. MEMORY_*)
├── config.py                      # Legacy config
├── database.py                    # SQLite async
├── requirements.txt
├── .env.example
│
├── memory/                        # Persistent Memory + HOPE Engine
│   ├── __init__.py                # exports AgentMemoryLayer, HopeEngine, HopeRule, UserProfile
│   ├── agent_memory.py            # AgentMemoryLayer: .md I/O, trim, stats, LLM prompt
│   ├── hope_engine.py             # NEW v3.3 — HopeRule + HopeEngine (evaluate/fire/digest)
│   ├── user_profile.py            # NEW v3.3 — UserProfile reads USER.md
│   ├── system/                   ← auto-created at runtime
│   │   ├── USER.md                # user Slack handle, timezone, per-priority channels
│   │   └── IDENTITY.md            # platform metadata
│   └── agents/                   ← auto-created at runtime
│       ├── {slug}/                # per-agent subdirectory (NEW v3.3)
│       │   ├── HOPE.md            # standing rules
│       │   ├── AGENTS.md          # agent relationships
│       │   ├── MEMORY.md          # task summaries
│       │   ├── SOUL.md            # agent personality
│       │   ├── TOOLS.md           # available tools
│       │   ├── IDENTITY.md        # agent metadata
│       │   └── logs/              # daily log files (YYYY-MM-DD.md)
│       ├── inter_agent_comms.md   # cross-agent event log (shared)
│       ├── task_history.md        # global compact audit table
│       └── system_state.md        # orchestrator snapshot (rewritten every 300s)
│
├── gateway/                       # Conversational Gateway (v3.1)
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

### v3.3.0 (Latest) — HOPE Engine Edition
- ✅ `memory/hope_engine.py` — `HopeRule` dataclass + `HopeEngine` with full rule lifecycle
- ✅ `memory/user_profile.py` — `UserProfile` parses `USER.md` for per-priority Slack channel routing
- ✅ `memory/system/USER.md` + `IDENTITY.md` — OpenClaw-style companion files
- ✅ Per-agent `memory/agents/{slug}/` subdirs — 6 companion files + `logs/` auto-created on first run
- ✅ `HopeEngine.evaluate()` runs on every `BaseAgent.process()` call (non-fatal)
- ✅ Mute hours (configurable `HOPE_MUTE_START/END_HOUR`), CRITICAL bypasses
- ✅ Rate limiting: `HOPE_MAX_ALERTS_PER_HOUR` rolling 60-min window per agent
- ✅ 4th routing tier in `gateway/router.py` — 9 HOPE trigger-phrase patterns
- ✅ `_handle_hope_create/cancel/list()` handlers in `webhook_handler.py`
- ✅ `format_hope_created/cancelled/list/alert()` in `formatter.py`
- ✅ CRITICAL alert format: `<!here>` + bold header + agent + condition + result preview
- ✅ 4 new `HOPE_*` settings; 3 new `/miq-hope*` slash commands
- ✅ Corrupt `HOPE.md` → file recreated from scratch; no exception propagates to agent

### v3.2.0 — Persistent Agent Memory Edition
- ✅ `memory/` package — `AgentMemoryLayer` with per-agent `.md` logs in `memory/agents/`
- ✅ Per-agent files: header line tracks entries / success rate / avg duration (O(1) read)
- ✅ Auto-trim: entries trimmed to `MEMORY_TRIM_TO` when count exceeds `MEMORY_MAX_ENTRIES_PER_AGENT`
- ✅ `inter_agent_comms.md` — every cross-agent event logged with source, subscribers, payload
- ✅ `task_history.md` — global audit table across all 19 agents (max 5 000 rows)
- ✅ `system_state.md` — orchestrator snapshot (queue, jobs, last 10 tasks) rewritten every 300 s
- ✅ `get_memory_context_prompt()` on `BaseAgent` — inject last N entries into any LLM system prompt
- ✅ Orchestrator `_handle_task_completion` returns triggered-event list; `update_last_entry_triggered` patches last `.md` entry
- ✅ 8 new `MEMORY_*` settings in `settings.py` — all have sensible defaults, work with zero config
- ✅ Failure-safe design: every memory call wrapped in `try/except`; missing `memory/` package never crashes agents

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

*Last Updated: February 2026 | MediaAgentIQ v3.3.0 — HOPE Engine Edition*
