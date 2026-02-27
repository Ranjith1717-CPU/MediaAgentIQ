"""
MediaAgentIQ Agents - AI-Powered Media Operations

Original 8 Agents (market-available features):
  CaptionAgent, ClipAgent, ArchiveAgent, ComplianceAgent,
  SocialPublishingAgent, LocalizationAgent, RightsAgent, TrendingAgent

Future-Ready Agents (market gaps - not yet available):
  DeepfakeDetectionAgent  - AI synthetic media detection for broadcasts
  LiveFactCheckAgent      - Real-time claim verification during live broadcasts
  AudienceIntelligenceAgent - Viewer retention prediction & drop-off prevention
  AIProductionDirectorAgent - Autonomous camera cuts, graphics, rundown optimization
  BrandSafetyAgent        - Real-time contextual ad safety scoring
  CarbonIntelligenceAgent - Broadcast carbon footprint tracking & ESG reporting

Phase 1 Pipeline Agents (broadcast pipeline gaps):
  IngestTranscodeAgent    - Media ingest & transcoding (FFmpeg / AWS MediaConvert)
  SignalQualityAgent      - EBU R128 loudness, black frame, freeze detection
  PlayoutSchedulingAgent  - Playout schedule & automation server integration
  OTTDistributionAgent    - HLS/DASH packaging, CDN publishing, multi-platform VOD
  NewsroomIntegrationAgent - iNews/ENPS MOS sync, wire ingestion, rundown management
"""
from .base_agent import BaseAgent, ProductionNotReadyError

# Original 8 agents
from .caption_agent import CaptionAgent
from .clip_agent import ClipAgent
from .archive_agent import ArchiveAgent
from .compliance_agent import ComplianceAgent
from .social_publishing_agent import SocialPublishingAgent
from .localization_agent import LocalizationAgent
from .rights_agent import RightsAgent
from .trending_agent import TrendingAgent

# Future-Ready Agents (Market Gaps)
from .deepfake_detection_agent import DeepfakeDetectionAgent
from .live_fact_check_agent import LiveFactCheckAgent
from .audience_intelligence_agent import AudienceIntelligenceAgent
from .ai_production_director_agent import AIProductionDirectorAgent
from .brand_safety_agent import BrandSafetyAgent
from .carbon_intelligence_agent import CarbonIntelligenceAgent

# Phase 1 Pipeline Agents (broadcast pipeline gaps)
from .ingest_transcode_agent import IngestTranscodeAgent
from .signal_quality_agent import SignalQualityAgent
from .playout_scheduling_agent import PlayoutSchedulingAgent
from .ott_distribution_agent import OTTDistributionAgent
from .newsroom_integration_agent import NewsroomIntegrationAgent

__all__ = [
    # Core
    "BaseAgent",
    "ProductionNotReadyError",
    # Original agents
    "CaptionAgent",
    "ClipAgent",
    "ArchiveAgent",
    "ComplianceAgent",
    "SocialPublishingAgent",
    "LocalizationAgent",
    "RightsAgent",
    "TrendingAgent",
    # Future-ready agents
    "DeepfakeDetectionAgent",
    "LiveFactCheckAgent",
    "AudienceIntelligenceAgent",
    "AIProductionDirectorAgent",
    "BrandSafetyAgent",
    "CarbonIntelligenceAgent",
    # Phase 1 pipeline agents
    "IngestTranscodeAgent",
    "SignalQualityAgent",
    "PlayoutSchedulingAgent",
    "OTTDistributionAgent",
    "NewsroomIntegrationAgent",
]

# Agent registry — used by gateway router and orchestrator
AGENTS = {
    # Original
    "caption":            CaptionAgent,
    "clip":               ClipAgent,
    "archive":            ArchiveAgent,
    "compliance":         ComplianceAgent,
    "social":             SocialPublishingAgent,
    "localization":       LocalizationAgent,
    "rights":             RightsAgent,
    "trending":           TrendingAgent,
    # Future-Ready
    "deepfake":           DeepfakeDetectionAgent,
    "fact_check":         LiveFactCheckAgent,
    "audience":           AudienceIntelligenceAgent,
    "production_director": AIProductionDirectorAgent,
    "brand_safety":       BrandSafetyAgent,
    "carbon":             CarbonIntelligenceAgent,
    # Phase 1 Pipeline
    "ingest_transcode":   IngestTranscodeAgent,
    "signal_quality":     SignalQualityAgent,
    "playout":            PlayoutSchedulingAgent,
    "ott":                OTTDistributionAgent,
    "newsroom":           NewsroomIntegrationAgent,
}
