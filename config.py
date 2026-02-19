"""
MediaAgentIQ Configuration

This module provides backward-compatible configuration constants
while integrating with the new Pydantic-based settings system.

For new code, prefer importing from settings.py:
    from settings import settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the new settings system
from settings import settings, Settings

# ==================== Base Paths ====================
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
DEMO_DATA_DIR = BASE_DIR / "demo_data"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
DEMO_DATA_DIR.mkdir(exist_ok=True)

# ==================== Mode Toggle ====================
# NEW: Use settings.PRODUCTION_MODE for mode detection
PRODUCTION_MODE = settings.PRODUCTION_MODE
USE_MOCK_AI = not settings.PRODUCTION_MODE  # Backward compatibility

# ==================== Database ====================
DATABASE_URL = settings.DATABASE_URL
DATABASE_PATH = BASE_DIR / "mediaagentiq.db"

# ==================== OpenAI ====================
OPENAI_API_KEY = settings.OPENAI_API_KEY or ""
OPENAI_MODEL = settings.OPENAI_MODEL
OPENAI_WHISPER_MODEL = settings.OPENAI_WHISPER_MODEL

# ==================== ElevenLabs ====================
ELEVENLABS_API_KEY = settings.ELEVENLABS_API_KEY or ""
ELEVENLABS_VOICE_ID = settings.ELEVENLABS_VOICE_ID

# ==================== Avid Media Central ====================
AVID_HOST = settings.AVID_HOST
AVID_USERNAME = settings.AVID_USERNAME
AVID_PASSWORD = settings.AVID_PASSWORD
AVID_WORKSPACE = settings.AVID_WORKSPACE
AVID_MOCK_MODE = settings.AVID_MOCK_MODE

# ==================== NMOS / Grass Valley ====================
NMOS_REGISTRY_URL = settings.NMOS_REGISTRY_URL
NMOS_NODE_ID = settings.NMOS_NODE_ID
NMOS_ENABLED = settings.NMOS_ENABLED

# ==================== Server Settings ====================
HOST = settings.HOST
PORT = settings.PORT
DEBUG = settings.DEBUG

# ==================== File Upload Settings ====================
MAX_UPLOAD_SIZE = settings.max_upload_size_bytes
ALLOWED_VIDEO_EXTENSIONS = settings.video_extensions
ALLOWED_AUDIO_EXTENSIONS = settings.audio_extensions

# ==================== Agent Settings ====================
CAPTION_CONFIDENCE_THRESHOLD = settings.CAPTION_CONFIDENCE_THRESHOLD
CLIP_MIN_DURATION = settings.CLIP_MIN_DURATION
CLIP_MAX_DURATION = settings.CLIP_MAX_DURATION
COMPLIANCE_SEVERITY_LEVELS = ["low", "medium", "high", "critical"]

# ==================== API Timeouts ====================
API_TIMEOUT_SECONDS = settings.API_TIMEOUT_SECONDS
TRANSCRIPTION_TIMEOUT_SECONDS = settings.TRANSCRIPTION_TIMEOUT_SECONDS


def get_settings() -> Settings:
    """Get the current settings instance."""
    return settings


def is_production_ready() -> bool:
    """Check if the system is ready for production mode."""
    if not PRODUCTION_MODE:
        return True  # Demo mode is always ready

    # In production mode, check required integrations
    return settings.is_openai_configured


def get_integration_status() -> dict:
    """Get status of all integrations."""
    return settings.get_integration_status()


# ==================== Export for backward compatibility ====================
__all__ = [
    # Mode
    "PRODUCTION_MODE",
    "USE_MOCK_AI",
    # Paths
    "BASE_DIR",
    "UPLOAD_DIR",
    "OUTPUT_DIR",
    "DEMO_DATA_DIR",
    # Database
    "DATABASE_URL",
    "DATABASE_PATH",
    # OpenAI
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "OPENAI_WHISPER_MODEL",
    # ElevenLabs
    "ELEVENLABS_API_KEY",
    "ELEVENLABS_VOICE_ID",
    # Avid
    "AVID_HOST",
    "AVID_USERNAME",
    "AVID_PASSWORD",
    "AVID_WORKSPACE",
    "AVID_MOCK_MODE",
    # NMOS
    "NMOS_REGISTRY_URL",
    "NMOS_NODE_ID",
    "NMOS_ENABLED",
    # Server
    "HOST",
    "PORT",
    "DEBUG",
    # Upload
    "MAX_UPLOAD_SIZE",
    "ALLOWED_VIDEO_EXTENSIONS",
    "ALLOWED_AUDIO_EXTENSIONS",
    # Agents
    "CAPTION_CONFIDENCE_THRESHOLD",
    "CLIP_MIN_DURATION",
    "CLIP_MAX_DURATION",
    "COMPLIANCE_SEVERITY_LEVELS",
    # Timeouts
    "API_TIMEOUT_SECONDS",
    "TRANSCRIPTION_TIMEOUT_SECONDS",
    # Functions
    "get_settings",
    "is_production_ready",
    "get_integration_status",
    # Settings class
    "settings",
    "Settings",
]
