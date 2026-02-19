"""
MediaAgentIQ Agents - AI-Powered Media Operations
"""
from .base_agent import BaseAgent, ProductionNotReadyError
from .caption_agent import CaptionAgent
from .clip_agent import ClipAgent
from .archive_agent import ArchiveAgent
from .compliance_agent import ComplianceAgent
from .social_publishing_agent import SocialPublishingAgent
from .localization_agent import LocalizationAgent
from .rights_agent import RightsAgent
from .trending_agent import TrendingAgent

__all__ = [
    "BaseAgent",
    "ProductionNotReadyError",
    "CaptionAgent",
    "ClipAgent",
    "ArchiveAgent",
    "ComplianceAgent",
    "SocialPublishingAgent",
    "LocalizationAgent",
    "RightsAgent",
    "TrendingAgent"
]

# Agent registry for easy access
AGENTS = {
    "caption": CaptionAgent,
    "clip": ClipAgent,
    "archive": ArchiveAgent,
    "compliance": ComplianceAgent,
    "social": SocialPublishingAgent,
    "localization": LocalizationAgent,
    "rights": RightsAgent,
    "trending": TrendingAgent
}
