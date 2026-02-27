"""
MediaAgentIQ — Gateway Router

Routes incoming user messages (from Slack, Teams, etc.)
to the correct agent using NLP intent detection.

Two routing paths:
  1. Slash commands  → deterministic parser → direct agent dispatch
  2. Natural language → Claude LLM → intent classification → agent dispatch

Supported intents → agents:
  caption            → CaptionAgent
  clip / viral       → ClipAgent
  compliance / fcc   → ComplianceAgent
  archive / search   → ArchiveAgent
  social / post      → SocialPublishingAgent
  localize / translate → LocalizationAgent
  rights / license   → RightsAgent
  trending / news    → TrendingAgent
  deepfake / verify  → DeepfakeDetectionAgent
  factcheck / fact   → LiveFactCheckAgent
  audience / viewers → AudienceIntelligenceAgent
  production / cues  → AIProductionDirectorAgent
  brand / ads        → BrandSafetyAgent
  carbon / esg       → CarbonIntelligenceAgent
  ingest / transcode → IngestTranscodeAgent
  signal / quality   → SignalQualityAgent
  playout / schedule → PlayoutSchedulingAgent
  ott / stream       → OTTDistributionAgent
  newsroom / rundown → NewsroomIntegrationAgent
  status / agents    → System status (no agent)
  connectors / mcp   → Connector dashboard (no agent)
"""

import re
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("gateway.router")


# ─── Intent dataclass ─────────────────────────────────────────────────────────

@dataclass
class RoutedIntent:
    """Result of routing a user message to an agent."""
    agent_key: Optional[str]        # key into AGENTS registry (or None for system)
    intent: str                     # human-readable intent label
    params: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0         # 1.0 for slash commands, 0-1 for NLP
    original_message: str = ""
    is_system_command: bool = False  # status / connectors dashboards
    system_command: Optional[str] = None


# ─── Agent routing map ────────────────────────────────────────────────────────

# keyword patterns → agent_key
_KEYWORD_MAP: List[tuple] = [
    # New Phase 1 agents (higher specificity first)
    (r"\b(ingest|transcode|encoding|proxy|format.convert)\b",  "ingest_transcode"),
    (r"\b(signal|loudness|blackframe|freeze|ebu.r128|qc.signal)\b", "signal_quality"),
    (r"\b(playout|scheduling|playlist|automation|scte|break.timing)\b", "playout"),
    (r"\b(ott|stream(ing)?|hls|dash|cdn|vod|multi.platform|distribute)\b", "ott"),
    (r"\b(newsroom|rundown|mos|inews|enps|wire|assignment)\b", "newsroom"),
    # Original agents
    (r"\b(caption|transcri(be|ption)|subtitle|srt|vtt|closed.caption)\b", "caption"),
    (r"\b(clip|viral|moment|highlight|reel)\b", "clip"),
    (r"\b(compliance|fcc|profanity|political.ad|eas|sponsorship)\b", "compliance"),
    (r"\b(archive|search|find|lookup|asset|mam|library)\b", "archive"),
    (r"\b(social|post|tweet|instagram|tiktok|facebook|youtube|publish)\b", "social"),
    (r"\b(locali(ze|se|zation)|translate|translation|dub(bing)?|language)\b", "localization"),
    (r"\b(rights|license|licence|dmca|copyright|violation|expir)\b", "rights"),
    (r"\b(trend(ing)?|breaking.news|monitor|wire)\b", "trending"),
    (r"\b(deepfake|synthetic|fake|ai.generat|forensic|authentic)\b", "deepfake"),
    (r"\b(fact.?check|verify|claim|misinform|false)\b", "fact_check"),
    (r"\b(audience|viewer|retention|drop.?off|rating)\b", "audience"),
    (r"\b(production|director|camera|lower.third|chyron|rundown.live)\b", "production_director"),
    (r"\b(brand.?safety|garm|ad.safe|advertiser|cpm)\b", "brand_safety"),
    (r"\b(carbon|esg|emission|ghg|sustainab|energy)\b", "carbon"),
]

# slash command → agent_key + param extractor
_SLASH_MAP: Dict[str, str] = {
    "/miq-caption":     "caption",
    "/miq-clip":        "clip",
    "/miq-compliance":  "compliance",
    "/miq-archive":     "archive",
    "/miq-social":      "social",
    "/miq-localize":    "localization",
    "/miq-rights":      "rights",
    "/miq-trending":    "trending",
    "/miq-deepfake":    "deepfake",
    "/miq-factcheck":   "fact_check",
    "/miq-audience":    "audience",
    "/miq-production":  "production_director",
    "/miq-brand":       "brand_safety",
    "/miq-carbon":      "carbon",
    "/miq-ingest":      "ingest_transcode",
    "/miq-signal":      "signal_quality",
    "/miq-playout":     "playout",
    "/miq-ott":         "ott",
    "/miq-newsroom":    "newsroom",
    # System commands
    "/miq-status":      "__status__",
    "/miq-connectors":  "__connectors__",
    "/miq-help":        "__help__",
}


# ─── Slash command parser ─────────────────────────────────────────────────────

def _parse_slash_command(text: str) -> RoutedIntent:
    """
    Parse a slash command into a RoutedIntent.

    Supports:
      /miq-compliance https://cdn.example.com/clip.mp4
      /miq-trending --live --topic=elections
      /miq-caption --url=https://... --language=en
      /miq-factcheck The president said X
    """
    parts = text.strip().split()
    command = parts[0].lower()
    agent_key_or_sys = _SLASH_MAP.get(command)

    if not agent_key_or_sys:
        return RoutedIntent(
            agent_key=None,
            intent="unknown_slash",
            confidence=1.0,
            original_message=text,
        )

    # System command
    if agent_key_or_sys.startswith("__"):
        sys_cmd = agent_key_or_sys.strip("_")
        return RoutedIntent(
            agent_key=None,
            intent=sys_cmd,
            is_system_command=True,
            system_command=sys_cmd,
            original_message=text,
        )

    # Parse flags: --key=value or --flag (boolean)
    params: Dict[str, Any] = {}
    positional: List[str] = []

    for part in parts[1:]:
        if part.startswith("--"):
            inner = part[2:]
            if "=" in inner:
                k, v = inner.split("=", 1)
                params[k] = v
            else:
                params[inner] = True
        else:
            positional.append(part)

    if positional:
        # First positional is usually a URL or free text
        first = positional[0]
        if first.startswith("http"):
            params["url"] = " ".join(positional)
        else:
            params["text"] = " ".join(positional)

    return RoutedIntent(
        agent_key=agent_key_or_sys,
        intent=agent_key_or_sys.replace("_", " "),
        params=params,
        confidence=1.0,
        original_message=text,
    )


# ─── Keyword NLP router ───────────────────────────────────────────────────────

def _route_by_keywords(text: str) -> RoutedIntent:
    """
    Match natural language message to an agent using keyword regex.
    Falls back to None if no match.
    """
    lower = text.lower()

    for pattern, agent_key in _KEYWORD_MAP:
        if re.search(pattern, lower):
            # Extract URL if present
            params: Dict[str, Any] = {}
            url_match = re.search(r"https?://\S+", text)
            if url_match:
                params["url"] = url_match.group()

            # Extract quoted text
            quoted = re.findall(r'"([^"]+)"', text)
            if quoted:
                params["text"] = quoted[0]

            return RoutedIntent(
                agent_key=agent_key,
                intent=agent_key.replace("_", " "),
                params=params,
                confidence=0.85,
                original_message=text,
            )

    # System commands in natural language
    if re.search(r"\b(status|health|agents)\b", lower):
        return RoutedIntent(
            agent_key=None,
            intent="status",
            is_system_command=True,
            system_command="status",
            original_message=text,
        )
    if re.search(r"\b(connector|integration|connected)\b", lower):
        return RoutedIntent(
            agent_key=None,
            intent="connectors",
            is_system_command=True,
            system_command="connectors",
            original_message=text,
        )
    if re.search(r"\b(help|what can|commands?|how to)\b", lower):
        return RoutedIntent(
            agent_key=None,
            intent="help",
            is_system_command=True,
            system_command="help",
            original_message=text,
        )

    return RoutedIntent(
        agent_key=None,
        intent="unrecognized",
        confidence=0.0,
        original_message=text,
    )


# ─── LLM-enhanced router ──────────────────────────────────────────────────────

async def _route_by_llm(text: str, history: List[Dict] = None) -> RoutedIntent:
    """
    Use Claude to classify intent when keyword matching fails or is ambiguous.
    Falls back to keyword result if OpenAI is not configured.
    """
    try:
        from settings import settings
        if not settings.is_openai_configured:
            return _route_by_keywords(text)

        import openai
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        agent_list = "\n".join(
            f"  - {k}" for k in [
                "caption", "clip", "compliance", "archive", "social",
                "localization", "rights", "trending", "deepfake", "fact_check",
                "audience", "production_director", "brand_safety", "carbon",
                "ingest_transcode", "signal_quality", "playout", "ott", "newsroom",
                "__status__", "__connectors__", "__help__",
            ]
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a media broadcast AI dispatcher. "
                    "Given a user message, return ONLY the agent key (one of the list below) "
                    "and optionally a JSON params object on a second line. "
                    "If you extract a URL, include it as {\"url\": \"...\"}. "
                    "If extracting text content, include {\"text\": \"...\"}.\n\n"
                    f"Available agents:\n{agent_list}"
                )
            }
        ]

        if history:
            messages.extend(history[-4:])

        messages.append({"role": "user", "content": text})

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=100,
            temperature=0,
        )

        raw = response.choices[0].message.content.strip()
        lines = raw.split("\n", 1)
        agent_key = lines[0].strip().lower()

        import json
        params = {}
        if len(lines) > 1:
            try:
                params = json.loads(lines[1])
            except Exception:
                pass

        if agent_key.startswith("__"):
            sys_cmd = agent_key.strip("_")
            return RoutedIntent(
                agent_key=None,
                intent=sys_cmd,
                is_system_command=True,
                system_command=sys_cmd,
                params=params,
                confidence=0.95,
                original_message=text,
            )

        return RoutedIntent(
            agent_key=agent_key,
            intent=agent_key.replace("_", " "),
            params=params,
            confidence=0.95,
            original_message=text,
        )

    except Exception as e:
        logger.warning(f"LLM routing failed, falling back to keyword match: {e}")
        return _route_by_keywords(text)


# ─── Main router ─────────────────────────────────────────────────────────────

async def route(
    text: str,
    conversation_history: List[Dict] = None
) -> RoutedIntent:
    """
    Route a user message to the appropriate agent.

    Routing priority:
    1. Slash command (/miq-*) → deterministic, instant
    2. Keyword match → fast, no API call
    3. LLM classification (Claude) → for ambiguous / complex requests
    """
    text = text.strip()

    # 1. Slash command
    if text.startswith("/miq-"):
        return _parse_slash_command(text)

    # 2. Keyword match
    keyword_result = _route_by_keywords(text)
    if keyword_result.confidence >= 0.85:
        return keyword_result

    # 3. LLM fallback for unrecognized or ambiguous
    return await _route_by_llm(text, history=conversation_history)


# ─── Help text ────────────────────────────────────────────────────────────────

HELP_TEXT = """
*MediaAgentIQ — Available Commands*

*Slash Commands (power users):*
• `/miq-caption [url]` — Generate captions
• `/miq-compliance [url]` — FCC compliance scan
• `/miq-clip [url]` — Detect viral moments
• `/miq-trending [--live] [--topic=X]` — Trending topics
• `/miq-deepfake [url]` — Deepfake detection
• `/miq-factcheck [text]` — Fact-check a claim
• `/miq-social [url]` — Generate social posts
• `/miq-archive [query]` — Search media archive
• `/miq-brand [url]` — Brand safety score
• `/miq-ingest [url]` — Ingest & transcode
• `/miq-signal [stream_url]` — Signal quality check
• `/miq-playout` — Playout schedule
• `/miq-ott [url]` — Publish to OTT/streaming
• `/miq-newsroom` — Sync newsroom rundown
• `/miq-status` — Agent health dashboard
• `/miq-connectors` — Connector status

*Natural language — just ask:*
• "Check compliance on today's 6pm newscast"
• "What's trending right now?"
• "Translate this clip to Spanish"
• "Is this video a deepfake?"
• "Generate social posts for the election coverage"
""".strip()
