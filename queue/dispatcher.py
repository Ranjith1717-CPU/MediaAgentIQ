"""
Agent dispatcher — maps agent_key strings to singleton agent instances
and provides a single entry-point for executing agent tasks.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

logger = logging.getLogger("runtime.dispatcher")

# ---------------------------------------------------------------------------
# Agent registry — lazy-initialised singletons
# ---------------------------------------------------------------------------

_AGENT_REGISTRY: Dict[str, Any] = {}


def _get_agent(agent_key: str) -> Any:
    """Return (or build) the singleton for agent_key."""
    if agent_key not in _AGENT_REGISTRY:
        _AGENT_REGISTRY[agent_key] = _build_agent(agent_key)
    return _AGENT_REGISTRY[agent_key]


def _build_agent(agent_key: str) -> Any:
    """Instantiate the correct agent class for agent_key."""
    # Original 8
    if agent_key == "caption":
        from agents.caption_agent import CaptionAgent
        return CaptionAgent()
    if agent_key == "clip":
        from agents.clip_agent import ClipAgent
        return ClipAgent()
    if agent_key == "compliance":
        from agents.compliance_agent import ComplianceAgent
        return ComplianceAgent()
    if agent_key == "archive":
        from agents.archive_agent import ArchiveAgent
        return ArchiveAgent()
    if agent_key == "social":
        from agents.social_publishing_agent import SocialPublishingAgent
        return SocialPublishingAgent()
    if agent_key == "localization":
        from agents.localization_agent import LocalizationAgent
        return LocalizationAgent()
    if agent_key == "rights":
        from agents.rights_agent import RightsAgent
        return RightsAgent()
    if agent_key == "trending":
        from agents.trending_agent import TrendingAgent
        return TrendingAgent()
    # Future-Ready 6
    if agent_key == "deepfake":
        from agents.deepfake_detection_agent import DeepfakeDetectionAgent
        return DeepfakeDetectionAgent()
    if agent_key == "fact_check":
        from agents.live_fact_check_agent import LiveFactCheckAgent
        return LiveFactCheckAgent()
    if agent_key == "audience":
        from agents.audience_intelligence_agent import AudienceIntelligenceAgent
        return AudienceIntelligenceAgent()
    if agent_key == "production_director":
        from agents.ai_production_director_agent import AIProductionDirectorAgent
        return AIProductionDirectorAgent()
    if agent_key == "brand_safety":
        from agents.brand_safety_agent import BrandSafetyAgent
        return BrandSafetyAgent()
    if agent_key == "carbon":
        from agents.carbon_intelligence_agent import CarbonIntelligenceAgent
        return CarbonIntelligenceAgent()
    # Phase 1 Pipeline 5
    if agent_key == "ingest_transcode":
        from agents.ingest_transcode_agent import IngestTranscodeAgent
        return IngestTranscodeAgent()
    if agent_key == "signal_quality":
        from agents.signal_quality_agent import SignalQualityAgent
        return SignalQualityAgent()
    if agent_key == "playout_scheduling":
        from agents.playout_scheduling_agent import PlayoutSchedulingAgent
        return PlayoutSchedulingAgent()
    if agent_key == "ott_distribution":
        from agents.ott_distribution_agent import OTTDistributionAgent
        return OTTDistributionAgent()
    if agent_key == "newsroom_integration":
        from agents.newsroom_integration_agent import NewsroomIntegrationAgent
        return NewsroomIntegrationAgent()

    raise ValueError(f"Unknown agent_key: '{agent_key}'")


# ---------------------------------------------------------------------------
# Public execute function
# ---------------------------------------------------------------------------

async def execute_agent_task(agent_key: str, input_data: Any) -> Dict[str, Any]:
    """
    Call agent.process(input_data) and return a normalised result dict.
    Always returns {"success": bool, "data": ..., "error": str|None}.
    """
    agent = _get_agent(agent_key)
    try:
        result = await agent.process(input_data)
        if isinstance(result, dict):
            return result
        return {"success": True, "data": result}
    except Exception as exc:
        logger.exception(f"Agent '{agent_key}' raised an exception: {exc}")
        return {"success": False, "error": str(exc), "data": None}


def list_registered_agents() -> list[str]:
    """Return all valid agent_key values."""
    return [
        "caption", "clip", "compliance", "archive", "social", "localization",
        "rights", "trending",
        "deepfake", "fact_check", "audience", "production_director",
        "brand_safety", "carbon",
        "ingest_transcode", "signal_quality", "playout_scheduling",
        "ott_distribution", "newsroom_integration",
    ]
