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

    # ==================== Future-Ready Agent Settings ====================

    # Deepfake Detection Agent
    DEEPFAKE_RISK_THRESHOLD: float = Field(
        default=0.60,
        description="Risk score above which content is flagged as likely synthetic (0.0-1.0)"
    )
    DEEPFAKE_AUTO_HOLD: bool = Field(
        default=True,
        description="Automatically hold content from broadcast when deepfake score > DEEPFAKE_RISK_THRESHOLD"
    )
    DEEPFAKE_SENSITIVITY: str = Field(
        default="balanced",
        description="Detection sensitivity: 'strict' (fewer false negatives) | 'balanced' | 'lenient'"
    )

    # Live Fact-Check Agent
    FACT_CHECK_AUTO_ALERT: bool = Field(
        default=True,
        description="Automatically alert producers when false/misleading claims detected"
    )
    FACT_CHECK_CLAIM_MIN_CONFIDENCE: float = Field(
        default=0.70,
        description="Minimum confidence to include a fact-check verdict in alerts"
    )
    FACT_CHECK_DATABASES: str = Field(
        default="ap,reuters,politifact,factcheck_org,snopes",
        description="Comma-separated fact-check databases to query"
    )

    # Audience Intelligence Agent
    AUDIENCE_PREDICTION_INTERVAL_SECS: int = Field(
        default=300,
        description="How often to refresh audience retention predictions (seconds)"
    )
    AUDIENCE_DROP_OFF_ALERT_THRESHOLD: float = Field(
        default=0.04,
        description="Predicted retention drop % that triggers producer alert (0.04 = 4%)"
    )

    # AI Production Director Agent
    PRODUCTION_DIRECTOR_AUTO_ACCEPT: bool = Field(
        default=False,
        description="Auto-accept AI production decisions (lower-thirds, graphics). False = human approval required."
    )
    PRODUCTION_DIRECTOR_CAMERA_LATENCY_MS: int = Field(
        default=500,
        description="Delay before suggesting camera cut (allow human director to act first)"
    )

    # Brand Safety Agent
    BRAND_SAFETY_DEFAULT_FLOOR: int = Field(
        default=70,
        description="Default minimum brand safety score for ad insertion (0-100)"
    )
    BRAND_SAFETY_AUTO_BLOCK: bool = Field(
        default=True,
        description="Automatically block premium ad insertions when GARM critical flags detected"
    )
    BRAND_SAFETY_GARM_ENABLED: bool = Field(
        default=True,
        description="Enable GARM (Global Alliance for Responsible Media) standard compliance"
    )

    # Carbon Intelligence Agent
    CARBON_GRID_REGION: str = Field(
        default="US_Northeast",
        description="Electricity grid region for carbon intensity calculation"
    )
    CARBON_REPORTING_INTERVAL_SECS: int = Field(
        default=1800,
        description="How often to update carbon footprint metrics (seconds)"
    )
    CARBON_ESG_REPORT_ENABLED: bool = Field(
        default=True,
        description="Enable automatic ESG report generation"
    )
    CARBON_RENEWABLE_PPA: float = Field(
        default=0.0,
        description="Percentage of electricity from renewable PPAs (0.0-100.0)"
    )

    # ==================== Slack Channel Connector ====================
    SLACK_BOT_TOKEN: Optional[str] = Field(
        default=None,
        description="Slack Bot User OAuth Token (xoxb-...) for sending messages"
    )
    SLACK_SIGNING_SECRET: Optional[str] = Field(
        default=None,
        description="Slack app signing secret for webhook verification"
    )
    SLACK_DEFAULT_CHANNEL: str = Field(
        default="#mediaagentiq",
        description="Default Slack channel for proactive agent alerts"
    )

    # ==================== Teams Channel Connector ====================
    TEAMS_APP_ID: Optional[str] = Field(
        default=None,
        description="Microsoft Teams Bot app registration ID (Azure AD)"
    )
    TEAMS_APP_PASSWORD: Optional[str] = Field(
        default=None,
        description="Microsoft Teams Bot app registration password"
    )
    TEAMS_TENANT_ID: str = Field(
        default="common",
        description="Azure AD tenant ID for Teams Bot authentication"
    )

    # ==================== Phase 1 Pipeline Agent Settings ====================

    # Ingest & Transcode Agent
    INGEST_DEFAULT_PROFILES: str = Field(
        default="broadcast_hd,proxy_edit,web_mp4",
        description="Comma-separated default transcode profiles for ingest"
    )
    INGEST_USE_CLOUD: bool = Field(
        default=False,
        description="Use AWS MediaConvert (true) vs local FFmpeg (false)"
    )
    AWS_MEDIACONVERT_ENDPOINT: Optional[str] = Field(
        default=None,
        description="AWS MediaConvert endpoint URL"
    )
    AWS_MEDIACONVERT_ROLE_ARN: Optional[str] = Field(
        default=None,
        description="IAM role ARN for AWS MediaConvert"
    )

    # Signal Quality Agent
    SIGNAL_QUALITY_LOUDNESS_TARGET_LUFS: float = Field(
        default=-23.0,
        description="Target integrated loudness for EBU R128 compliance (LUFS)"
    )
    SIGNAL_QUALITY_TRUE_PEAK_LIMIT: float = Field(
        default=-1.0,
        description="Maximum true peak level in dBTP (EBU R128)"
    )
    SIGNAL_QUALITY_ALERT_ON_CRITICAL: bool = Field(
        default=True,
        description="Send Slack/Teams alert on critical signal quality issues"
    )

    # Playout & Scheduling Agent
    AUTOMATION_SERVER_URL: Optional[str] = Field(
        default=None,
        description="Playout automation server REST API URL (Harmonic / GV Maestro)"
    )
    AUTOMATION_SERVER_TYPE: str = Field(
        default="harmonic",
        description="Automation server type: harmonic | gv_maestro | ross_overdrive"
    )

    # OTT Distribution Agent
    CDN_PROVIDER: str = Field(
        default="cloudfront",
        description="Default CDN provider: cloudfront | akamai | fastly"
    )
    CDN_ORIGIN_URL: Optional[str] = Field(
        default=None,
        description="CDN origin server URL"
    )
    OTT_DRM_ENABLED: bool = Field(
        default=False,
        description="Enable DRM on HLS/DASH streams"
    )
    AWS_MEDIAPACKAGE_CHANNEL_ID: Optional[str] = Field(
        default=None,
        description="AWS MediaPackage channel ID for HLS/DASH packaging"
    )

    # Newsroom Integration Agent
    INEWS_API_URL: Optional[str] = Field(
        default=None,
        description="iNews REST API base URL"
    )
    ENPS_API_URL: Optional[str] = Field(
        default=None,
        description="ENPS REST API base URL (alternative to iNews)"
    )
    NEWSROOM_SYNC_INTERVAL_SECS: int = Field(
        default=180,
        description="How often to sync rundown from newsroom system (seconds)"
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

    @property
    def fact_check_databases_list(self) -> list:
        """Get fact-check databases as a list."""
        return [db.strip() for db in self.FACT_CHECK_DATABASES.split(",")]

    @property
    def is_deepfake_strict_mode(self) -> bool:
        """Check if deepfake detection is in strict mode."""
        return self.DEEPFAKE_SENSITIVITY == "strict"

    def get_integration_status(self) -> dict:
        """Get status of all integrations."""
        return {
            # Original integrations
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
            },
            # Future-Ready agent configurations
            "deepfake_detection": {
                "risk_threshold": self.DEEPFAKE_RISK_THRESHOLD,
                "auto_hold": self.DEEPFAKE_AUTO_HOLD,
                "sensitivity": self.DEEPFAKE_SENSITIVITY,
                "production_ready": self.is_openai_configured and self.PRODUCTION_MODE
            },
            "live_fact_check": {
                "auto_alert": self.FACT_CHECK_AUTO_ALERT,
                "databases": self.fact_check_databases_list,
                "min_confidence": self.FACT_CHECK_CLAIM_MIN_CONFIDENCE,
                "production_ready": self.is_openai_configured and self.PRODUCTION_MODE
            },
            "audience_intelligence": {
                "prediction_interval_secs": self.AUDIENCE_PREDICTION_INTERVAL_SECS,
                "drop_off_threshold": self.AUDIENCE_DROP_OFF_ALERT_THRESHOLD,
                "production_ready": self.PRODUCTION_MODE
            },
            "ai_production_director": {
                "auto_accept": self.PRODUCTION_DIRECTOR_AUTO_ACCEPT,
                "camera_latency_ms": self.PRODUCTION_DIRECTOR_CAMERA_LATENCY_MS,
                "production_ready": self.is_openai_configured and self.PRODUCTION_MODE
            },
            "brand_safety": {
                "safety_floor": self.BRAND_SAFETY_DEFAULT_FLOOR,
                "auto_block": self.BRAND_SAFETY_AUTO_BLOCK,
                "garm_enabled": self.BRAND_SAFETY_GARM_ENABLED,
                "production_ready": self.is_openai_configured and self.PRODUCTION_MODE
            },
            "carbon_intelligence": {
                "grid_region": self.CARBON_GRID_REGION,
                "reporting_interval_secs": self.CARBON_REPORTING_INTERVAL_SECS,
                "renewable_ppa_pct": self.CARBON_RENEWABLE_PPA,
                "production_ready": self.PRODUCTION_MODE
            }
        }


# Create singleton instance
settings = Settings()


# Export for easy import
__all__ = ["Settings", "settings", "BroadcastSystem"]
