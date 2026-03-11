# MediaAgentIQ — Live Runtime Go-Live Guide

## Overview

This guide covers starting the Redis-backed runtime layer, verifying health,
and running the smoke test sequence. The existing demo/Streamlit paths are
unaffected; all new endpoints are additive.

---

## Option A: Local (SQLite + no Docker)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run database migrations
```bash
alembic upgrade head
```
Creates `runtime.db` (SQLite) with tables: `tasks`, `task_events`, `dead_letters`, `worker_heartbeats`.

### 3. Start Redis (required for queue + SSE)
```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis

# Docker (easiest)
docker run -d -p 6379:6379 --name miq-redis redis:7-alpine
```

### 4. Start the API server (terminal 1)
```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```
Expected log: `Runtime tables ready.` + `✅ MediaAgentIQ started successfully!`

### 5. Start the worker (terminal 2)
```bash
python worker_runtime.py
```
Expected log: `Worker worker-<hostname>-<pid>-<hex> starting — concurrency=4`

---

## Option B: Production (Docker Compose)

### 1. Create `.env` from example
```bash
cp .env.example .env
# Edit: POSTGRES_PASSWORD, OPENAI_API_KEY, SLACK_BOT_TOKEN, etc.
```

### 2. Launch all services
```bash
docker compose -f docker-compose.prod.yml up -d
```

### 3. Check service status
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs api --tail=50
docker compose -f docker-compose.prod.yml logs worker --tail=50
```

---

## Smoke Test Sequence

### Step 1 — Health check
```bash
curl http://localhost:8000/ops/health
```
Expected:
```json
{"redis": "ok", "db": "ok", "worker_count": 1, "status": "healthy"}
```

### Step 2 — Submit a task
```bash
curl -X POST http://localhost:8000/api/tasks/submit \
  -H "Content-Type: application/json" \
  -d '{"agent_key": "compliance", "input_data": {"mode": "monitor"}, "priority": "HIGH"}'
```
Expected:
```json
{"task_id": "abc123-...", "status": "QUEUED", "agent_key": "compliance", "priority": "HIGH"}
```

### Step 3 — Watch SSE stream (terminal 3)
```bash
# Replace abc123 with actual task_id from Step 2
curl -N http://localhost:8000/api/realtime/events?task_id=abc123
```
Expected events:
```
data: {"task_id": "abc123", "event": "running", ...}
data: {"task_id": "abc123", "event": "completed", ...}
```

### Step 4 — Poll task status
```bash
curl http://localhost:8000/api/tasks/abc123
```
Expected `"status": "COMPLETED"` with `output_data`.

### Step 5 — Cancel a queued task
```bash
# Submit a new task first
TASK_ID=$(curl -s -X POST http://localhost:8000/api/tasks/submit \
  -H "Content-Type: application/json" \
  -d '{"agent_key": "caption", "input_data": {}}' | python -c "import sys,json; print(json.load(sys.stdin)['task_id'])")

# Cancel immediately
curl -X POST http://localhost:8000/ops/cancel/$TASK_ID
```
Expected: `{"task_id": "...", "cancelled": true}`

### Step 6 — View dead-letter queue
```bash
curl http://localhost:8000/ops/dlq
```

### Step 7 — Replay a dead-letter entry
```bash
# Replace 1 with actual DLQ entry id
curl -X POST http://localhost:8000/ops/replay/1
```
Expected: `{"replayed": true, "dlq_id": 1, "new_task_id": "..."}`

---

## Configuration Reference (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |
| `RUNTIME_DATABASE_URL` | `sqlite+aiosqlite:///runtime.db` | SQLAlchemy async URL |
| `TASK_MAX_RETRIES` | `3` | Retries before DLQ |
| `TASK_RETRY_BACKOFF_SECONDS` | `5` | Base backoff per retry |
| `WORKER_CONCURRENCY` | `4` | Parallel tasks per worker |
| `WORKER_HEARTBEAT_INTERVAL_SECS` | `30` | Heartbeat frequency |
| `AGENT_TIMEOUT_JSON` | `{}` | Per-agent timeouts, e.g. `{"deepfake":90}` |
| `RUNTIME_SSE_KEEPALIVE_SECS` | `15` | SSE keepalive ping interval |

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/tasks/submit` | Submit a new agent task |
| `GET`  | `/api/tasks/{task_id}` | Poll task status |
| `GET`  | `/api/realtime/events?task_id=` | SSE event stream |
| `POST` | `/ops/cancel/{task_id}` | Cancel a task |
| `GET`  | `/ops/dlq` | List dead-letter entries |
| `POST` | `/ops/replay/{dlq_id}` | Replay a dead-letter entry |
| `GET`  | `/ops/health` | System health check |

---

## Backward Compatibility

The following are **untouched** by this runtime layer:
- `database.py` — original aiosqlite helpers
- `orchestrator.py` — in-memory asyncio deque
- `streamlit_app.py` — Streamlit UI
- All existing `/api/caption/process`, `/api/clip/process`, etc. routes
- Demo mode — works with zero API keys and no Redis (new routers fail gracefully with a startup warning)
