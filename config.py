"""
MediaAgentIQ Configuration
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
DEMO_DATA_DIR = BASE_DIR / "demo_data"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
DEMO_DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/mediaagentiq.db"
DATABASE_PATH = BASE_DIR / "mediaagentiq.db"

# OpenAI (optional - uses mock by default)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_MOCK_AI = not OPENAI_API_KEY  # Use mock responses if no API key

# Server settings
HOST = "127.0.0.1"
PORT = 8000
DEBUG = True

# File upload settings
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac"}

# Agent settings
CAPTION_CONFIDENCE_THRESHOLD = 0.85
CLIP_MIN_DURATION = 15  # seconds
CLIP_MAX_DURATION = 60  # seconds
COMPLIANCE_SEVERITY_LEVELS = ["low", "medium", "high", "critical"]
