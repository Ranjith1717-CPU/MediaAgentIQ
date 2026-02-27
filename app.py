"""
MediaAgentIQ - AI Agent Platform for Media & Broadcast
Main FastAPI Application
"""
import os
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

# Import agents
from agents import (
    CaptionAgent, ClipAgent, ArchiveAgent, ComplianceAgent,
    SocialPublishingAgent, LocalizationAgent, RightsAgent, TrendingAgent
)
import database
from config import UPLOAD_DIR, OUTPUT_DIR, DEBUG

# Initialize FastAPI app
app = FastAPI(
    title="MediaAgentIQ",
    description="AI Agent Platform for Media & Broadcast Operations",
    version="3.1.0"
)

# Mount the channel gateway (Slack + Teams webhooks)
try:
    from gateway.webhook_handler import gateway_router
    app.include_router(gateway_router)
except Exception as _e:
    import logging as _logging
    _logging.getLogger("app").warning(f"Gateway router not loaded: {_e}")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize agents
caption_agent = CaptionAgent()
clip_agent = ClipAgent()
archive_agent = ArchiveAgent()
compliance_agent = ComplianceAgent()
social_agent = SocialPublishingAgent()
localization_agent = LocalizationAgent()
rights_agent = RightsAgent()
trending_agent = TrendingAgent()

# Agent info for dashboard
AGENTS_INFO = [
    {
        "id": "clip",
        "name": "Clip Agent",
        "icon": "🎬",
        "description": "Monitors live broadcasts, identifies viral moments, auto-creates social clips with captions",
        "benefit": "10x more social content, zero editing time",
        "color": "purple",
        "route": "/clip"
    },
    {
        "id": "caption",
        "name": "Caption Agent",
        "icon": "📝",
        "description": "Auto-generates captions, QA checks, fixes timing issues, delivers broadcast-ready files",
        "benefit": "80% reduction in captioning costs",
        "color": "blue",
        "route": "/caption"
    },
    {
        "id": "compliance",
        "name": "Compliance Agent",
        "icon": "⚖️",
        "description": "Monitors 24/7 for FCC violations, profanity, political ad issues, auto-logs and alerts",
        "benefit": "Avoid $500K+ fines",
        "color": "red",
        "route": "/compliance"
    },
    {
        "id": "archive",
        "name": "Archive Agent",
        "icon": "🔍",
        "description": "Answers natural language queries like \"Find all Biden economy clips from Q3\"",
        "benefit": "Instant archive access",
        "color": "green",
        "route": "/archive"
    },
    {
        "id": "social",
        "name": "Social Publishing Agent",
        "icon": "📱",
        "description": "Creates Twitter/Instagram/TikTok posts from broadcast highlights, schedules posting",
        "benefit": "Always-on social presence",
        "color": "pink",
        "route": "/social"
    },
    {
        "id": "localization",
        "name": "Localization Agent",
        "icon": "🌍",
        "description": "Auto-translates captions, generates dubs, manages multi-language workflows",
        "benefit": "Faster global distribution",
        "color": "cyan",
        "route": "/localization"
    },
    {
        "id": "rights",
        "name": "Rights Agent",
        "icon": "📜",
        "description": "Tracks content licenses, alerts before expiry, monitors unauthorized usage",
        "benefit": "Avoid legal disputes",
        "color": "orange",
        "route": "/rights"
    },
    {
        "id": "trending",
        "name": "Trending Agent",
        "icon": "📈",
        "description": "Monitors social media, news feeds, alerts newsroom to breaking/trending stories",
        "benefit": "Never miss a story",
        "color": "yellow",
        "route": "/trending"
    }
]


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    await database.init_database()
    print("✅ MediaAgentIQ started successfully!")
    print(f"🌐 Dashboard: http://127.0.0.1:8000")


# ============== Dashboard Routes ==============

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    stats = await database.get_stats()
    activity = await database.get_recent_activity(limit=5)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "agents": AGENTS_INFO,
        "stats": stats,
        "activity": activity
    })


# ============== Caption Agent Routes ==============

@app.get("/caption", response_class=HTMLResponse)
async def caption_page(request: Request):
    """Caption Agent page."""
    return templates.TemplateResponse("caption.html", {
        "request": request,
        "agent": caption_agent.get_info()
    })


@app.post("/api/caption/process")
async def process_caption(file: UploadFile = File(...)):
    """Process media file for captioning."""
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Create job
        job_id = await database.create_job("caption", str(file_path))
        await database.log_activity("caption", "started", f"Processing {file.filename}")

        # Process with agent
        result = await caption_agent.process(str(file_path))

        if result["success"]:
            # Save outputs
            output_base = OUTPUT_DIR / f"caption_{job_id}"
            srt_path = f"{output_base}.srt"
            vtt_path = f"{output_base}.vtt"

            with open(srt_path, "w") as f:
                f.write(result["data"]["srt"])
            with open(vtt_path, "w") as f:
                f.write(result["data"]["vtt"])

            await database.update_job(job_id, "completed", srt_path, json.dumps(result["data"]))
            await database.log_activity("caption", "completed", f"Generated captions for {file.filename}")

        return JSONResponse(result)

    except Exception as e:
        await database.log_activity("caption", "error", str(e))
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Clip Agent Routes ==============

@app.get("/clip", response_class=HTMLResponse)
async def clip_page(request: Request):
    """Clip Agent page."""
    return templates.TemplateResponse("clip.html", {
        "request": request,
        "agent": clip_agent.get_info()
    })


@app.post("/api/clip/process")
async def process_clip(file: UploadFile = File(...)):
    """Process video for viral clip detection."""
    try:
        file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        job_id = await database.create_job("clip", str(file_path))
        await database.log_activity("clip", "started", f"Analyzing {file.filename}")

        result = await clip_agent.process(str(file_path))

        if result["success"]:
            await database.update_job(job_id, "completed", None, json.dumps(result["data"]))
            await database.log_activity("clip", "completed", f"Found {len(result['data']['viral_moments'])} viral moments")

        return JSONResponse(result)

    except Exception as e:
        await database.log_activity("clip", "error", str(e))
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Archive Agent Routes ==============

@app.get("/archive", response_class=HTMLResponse)
async def archive_page(request: Request):
    """Archive Agent page."""
    return templates.TemplateResponse("archive.html", {
        "request": request,
        "agent": archive_agent.get_info()
    })


@app.post("/api/archive/search")
async def search_archive(request: Request):
    """Search archive with natural language."""
    try:
        data = await request.json()
        query = data.get("query", "")
        filters = data.get("filters", {})

        await database.log_activity("archive", "search", f"Query: {query}")

        result = await archive_agent.process({"query": query, "filters": filters})

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Compliance Agent Routes ==============

@app.get("/compliance", response_class=HTMLResponse)
async def compliance_page(request: Request):
    """Compliance Agent page."""
    return templates.TemplateResponse("compliance.html", {
        "request": request,
        "agent": compliance_agent.get_info()
    })


@app.post("/api/compliance/scan")
async def scan_compliance(file: UploadFile = File(None), transcript: str = Form(None)):
    """Scan content for compliance issues."""
    try:
        input_data = {}

        if file:
            file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            input_data["file"] = str(file_path)

        if transcript:
            input_data["transcript"] = transcript

        job_id = await database.create_job("compliance", input_data.get("file"))
        await database.log_activity("compliance", "scan_started", "Compliance scan initiated")

        result = await compliance_agent.process(input_data if input_data else "demo_scan")

        if result["success"]:
            await database.update_job(job_id, "completed", None, json.dumps(result["data"]))
            issues_count = len(result["data"].get("issues", []))
            await database.log_activity("compliance", "scan_completed", f"Found {issues_count} issues")

        return JSONResponse(result)

    except Exception as e:
        await database.log_activity("compliance", "error", str(e))
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Social Publishing Agent Routes ==============

@app.get("/social", response_class=HTMLResponse)
async def social_page(request: Request):
    """Social Publishing Agent page."""
    return templates.TemplateResponse("social.html", {
        "request": request,
        "agent": social_agent.get_info()
    })


@app.post("/api/social/generate")
async def generate_social_posts(request: Request):
    """Generate social media posts from content."""
    try:
        data = await request.json()
        await database.log_activity("social", "generate", "Generating social posts")

        result = await social_agent.process(data)

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Localization Agent Routes ==============

@app.get("/localization", response_class=HTMLResponse)
async def localization_page(request: Request):
    """Localization Agent page."""
    return templates.TemplateResponse("localization.html", {
        "request": request,
        "agent": localization_agent.get_info()
    })


@app.post("/api/localization/translate")
async def translate_content(request: Request):
    """Translate content to multiple languages."""
    try:
        data = await request.json()
        await database.log_activity("localization", "translate", f"Target languages: {data.get('target_languages', [])}")

        result = await localization_agent.process(data)

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Rights Agent Routes ==============

@app.get("/rights", response_class=HTMLResponse)
async def rights_page(request: Request):
    """Rights Agent page."""
    return templates.TemplateResponse("rights.html", {
        "request": request,
        "agent": rights_agent.get_info()
    })


@app.post("/api/rights/check")
async def check_rights(request: Request):
    """Check content rights and licenses."""
    try:
        data = await request.json()
        await database.log_activity("rights", "check", "Rights check initiated")

        result = await rights_agent.process(data)

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Trending Agent Routes ==============

@app.get("/trending", response_class=HTMLResponse)
async def trending_page(request: Request):
    """Trending Agent page."""
    return templates.TemplateResponse("trending.html", {
        "request": request,
        "agent": trending_agent.get_info()
    })


@app.post("/api/trending/monitor")
async def monitor_trends(request: Request):
    """Monitor trending topics and breaking news."""
    try:
        data = await request.json() if request.headers.get("content-type") == "application/json" else {}
        await database.log_activity("trending", "monitor", "Trend monitoring")

        result = await trending_agent.process(data)

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ============== Utility Routes ==============

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics."""
    stats = await database.get_stats()
    return JSONResponse(stats)


@app.get("/api/activity")
async def get_activity(limit: int = 10):
    """Get recent activity."""
    activity = await database.get_recent_activity(limit)
    return JSONResponse(activity)


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated file."""
    file_path = OUTPUT_DIR / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")


# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=DEBUG)
