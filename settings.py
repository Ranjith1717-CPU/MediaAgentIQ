"""
MediaAgentIQ Settings Module
Centralized, typed configuration with Pydantic BaseSettings

Supports:
- Environment variables
- .env file loading
- Type validation
- Default values for demo mode
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path
from enum import Enum


class BroadcastSystem(str, Enum):
    """Supported broadcast system integrations."""
    AVID = "avid"
    GRASS_VALLEY = "grass_valley"
    ROSS_VIDEO = "ross_video"
    VIZRT = "vizrt"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Usage:
        from settings import settings
        if settings.PRODUCTION_MODE:
            # Use real APIs
    """

    # ==================== Mode Toggle ====================
    PRODUCTION_MODE: bool = Field(
        default=False,
        description="True for production (real APIs), False for demo (mock data)"
    )

    # ==================== OpenAI Configuration ====================
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key for Whisper transcription and GPT-4"
    )
    OPENAI_MODEL: str = Field(
        default="gpt-4-turbo-preview",
        description="OpenAI model for text analysis"
    )
    OPENAI_WHISPER_MODEL: str = Field(
        default="whisper-1",
        description="OpenAI Whisper model for transcription"
    )

    # ==================== ElevenLabs Configuration ====================
    ELEVENLABS_API_KEY: Optional[str] = Field(
        default=None,
        description="ElevenLabs API key for voice dubbing"
    )
    ELEVENLABS_VOICE_ID: str = Field(
        default="21m00Tcm4TlvDq8ikWAM",
        description="Default ElevenLabs voice ID"
    )

    # ==================== Avid Media Central ====================
    AVID_HOST: Optional[str] = Field(
        default=None,
        description="Avid Media Central CTMS host URL"
    )
    AVID_USERNAME: Optional[str] = Field(
        default=None,
        description="Avid Media Central username"
    )
    AVID_PASSWORD: Optional[str] = Field(
        default=None,
        description="Avid Media Central password"
    )
    AVID_WORKSPACE: Optional[str] = Field(
        default=None,
        description="Avid Media Central default workspace"
    )
    AVID_MOCK_MODE: bool = Field(
        default=True,
        description="Use mock Avid responses (for development)"
    )

    # ==================== Grass Valley / NMOS ====================
    NMOS_REGISTRY_URL: Optional[str] = Field(
        default=None,
        description="NMOS IS-04 Registry URL for GV Orbit"
    )
    NMOS_NODE_ID: Optional[str] = Field(
        default=None,
        description="NMOS Node ID for this application"
    )
    NMOS_ENABLED: bool = Field(
        default=False,
        description="Enable NMOS integration"
    )

    # ==================== Database ====================
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///mediaagentiq.db",
        description="Database connection URL"
    )

    # ==================== Server Configuration ====================
    HOST: str = Field(default="127.0.0.1", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=True, description="Debug mode")

    # ==================== File Settings ====================
    MAX_UPLOAD_SIZE_MB: int = Field(
        default=100,
        description="Maximum upload size in megabytes"
    )
    ALLOWED_VIDEO_EXTENSIONS: str = Field(
        default=".mp4,.mov,.avi,.mkv,.webm",
        description="Comma-separated allowed video extensions"
    )
    ALLOWED_AUDIO_EXTENSIONS: str = Field(
        default=".mp3,.wav,.m4a,.aac",
        description="Comma-separated allowed audio extensions"
    )

    # ==================== Agent Settings ====================
    CAPTION_CONFIDENCE_THRESHOLD: float = Field(
        default=0.85,
        description="Minimum confidence for captions"
    )
    CLIP_MIN_DURATION: int = Field(
        default=15,
        description="Minimum clip duration in seconds"
    )
    CLIP_MAX_DURATION: int = Field(
        default=60,
        description="Maximum clip duration in seconds"
    )

    # ==================== API Timeouts ====================
    API_TIMEOUT_SECONDS: int = Field(
        default=30,
        description="Default API timeout in seconds"
    )
    TRANSCRIPTION_TIMEOUT_SECONDS: int = Field(
        default=300,
        description="Transcription API timeout (5 minutes)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

    # ==================== Helper Properties ====================

    @property
    def max_upload_size_bytes(self) -> int:
        """Get max upload size in bytes."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    @property
    def video_extensions(self) -> set:
        """Get allowed video extensions as a set."""
        return set(self.ALLOWED_VIDEO_EXTENSIONS.split(","))

    @property
    def audio_extensions(self) -> set:
        """Get allowed audio extensions as a set."""
        return set(self.ALLOWED_AUDIO_EXTENSIONS.split(","))

    @property
    def is_openai_configured(self) -> bool:
        """Check if OpenAI is properly configured."""
        return bool(self.OPENAI_API_KEY)

    @property
    def is_avid_configured(self) -> bool:
        """Check if Avid Media Central is configured."""
        return all([
            self.AVID_HOST,
            self.AVID_USERNAME,
            self.AVID_PASSWORD
        ])

    @property
    def is_nmos_configured(self) -> bool:
        """Check if NMOS is configured."""
        return bool(self.NMOS_REGISTRY_URL) and self.NMOS_ENABLED

    def get_integration_status(self) -> dict:
        """Get status of all integrations."""
        return {
            "openai": {
                "configured": self.is_openai_configured,
                "production_ready": self.is_openai_configured and self.PRODUCTION_MODE
            },
            "avid": {
                "configured": self.is_avid_configured,
                "mock_mode": self.AVID_MOCK_MODE,
                "production_ready": self.is_avid_configured and not self.AVID_MOCK_MODE
            },
            "nmos": {
                "configured": self.is_nmos_configured,
                "production_ready": self.is_nmos_configured and self.PRODUCTION_MODE
            },
            "elevenlabs": {
                "configured": bool(self.ELEVENLABS_API_KEY),
                "production_ready": bool(self.ELEVENLABS_API_KEY) and self.PRODUCTION_MODE
            }
        }


# Create singleton instance
settings = Settings()


# Export for easy import
__all__ = ["Settings", "settings", "BroadcastSystem"]
