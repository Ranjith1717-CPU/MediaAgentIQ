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
]

# Agent registry for easy access
AGENTS = {
    # Original
    "caption": CaptionAgent,
    "clip": ClipAgent,
    "archive": ArchiveAgent,
    "compliance": ComplianceAgent,
    "social": SocialPublishingAgent,
    "localization": LocalizationAgent,
    "rights": RightsAgent,
    "trending": TrendingAgent,
    # Future-Ready
    "deepfake": DeepfakeDetectionAgent,
    "fact_check": LiveFactCheckAgent,
    "audience": AudienceIntelligenceAgent,
    "production_director": AIProductionDirectorAgent,
    "brand_safety": BrandSafetyAgent,
    "carbon": CarbonIntelligenceAgent,
}
