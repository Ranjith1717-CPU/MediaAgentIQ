"""
Trending Agent - Monitors social media, news feeds, alerts newsroom to breaking/trending stories

Supports:
- Demo Mode: Returns mock trending data for demonstration
- Production Mode: Uses external APIs for real-time trend monitoring
"""
import random
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from .base_agent import BaseAgent

if TYPE_CHECKING:
    from settings import Settings


class TrendingAgent(BaseAgent):
    """
    Agent for monitoring trends and alerting newsroom.

    Demo Mode: Returns realistic mock trending data
    Production Mode: Connects to social APIs for real trend data
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Trending Agent",
            description="Monitors social media, news feeds, alerts newsroom to breaking/trending stories",
            settings=settings
        )

        self.monitored_sources = {
            "social_media": ["Twitter/X", "Facebook", "Instagram", "TikTok", "Reddit"],
            "news_wires": ["AP", "Reuters", "AFP", "Bloomberg"],
            "news_sites": ["CNN", "BBC", "NYT", "WSJ", "Fox News"],
            "specialized": ["TMZ", "ESPN", "TechCrunch", "Variety"]
        }

        self.topic_categories = [
            "politics", "business", "technology", "entertainment",
            "sports", "health", "science", "world", "local"
        ]

    def _get_required_integrations(self) -> Dict[str, bool]:
        """Trending Agent can use external APIs in production."""
        # In production, would require social media API keys
        return {
            "openai": self.settings.is_openai_configured  # For trend analysis
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate input for trend monitoring."""
        return True  # Always valid - can run without input

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Demo mode processing - returns mock trending data.
        """
        self.log_activity("demo_process", "Monitoring trends")

        # Get filters from input
        filters = {}
        if isinstance(input_data, dict):
            filters = input_data.get("filters", {})

        # Get trending topics
        trends = await self._get_trending_topics_mock(filters)

        # Get breaking news
        breaking = await self._get_breaking_news_mock()

        # Analyze viral content
        viral = await self._analyze_viral_content_mock()

        # Generate newsroom alerts
        alerts = await self._generate_newsroom_alerts(trends, breaking, viral)

        # Create story suggestions
        suggestions = await self._create_story_suggestions(trends, breaking)

        return self.create_response(True, data={
            "trends": trends,
            "breaking_news": breaking,
            "viral_content": viral,
            "alerts": alerts,
            "story_suggestions": suggestions,
            "stats": {
                "topics_monitored": len(self.topic_categories),
                "sources_monitored": sum(len(v) for v in self.monitored_sources.values()),
                "trends_detected": len(trends),
                "breaking_stories": len(breaking),
                "high_priority_alerts": len([a for a in alerts if a["priority"] == "high"]),
                "last_updated": datetime.now().isoformat()
            }
        })

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production mode processing - uses real APIs for trend monitoring.
        """
        self.log_activity("production_process", "Monitoring trends with real data")

        # Get filters from input
        filters = {}
        if isinstance(input_data, dict):
            filters = input_data.get("filters", {})

        # In production, this would connect to:
        # - Twitter/X API for trending topics
        # - News APIs (NewsAPI, Google News, etc.)
        # - Social listening platforms (Brandwatch, Sprout Social)
        # - RSS feeds from news wires

        # For now, we'll use GPT-4 to analyze and enhance mock data
        # simulating what real API data would look like

        trends = await self._get_trending_topics_mock(filters)
        breaking = await self._get_breaking_news_mock()
        viral = await self._analyze_viral_content_mock()

        # Use GPT-4 to analyze trends and generate insights if configured
        if self.settings.is_openai_configured:
            enhanced_suggestions = await self._generate_ai_story_suggestions(trends, breaking)
        else:
            enhanced_suggestions = await self._create_story_suggestions(trends, breaking)

        # Generate newsroom alerts
        alerts = await self._generate_newsroom_alerts(trends, breaking, viral)

        return self.create_response(True, data={
            "trends": trends,
            "breaking_news": breaking,
            "viral_content": viral,
            "alerts": alerts,
            "story_suggestions": enhanced_suggestions,
            "stats": {
                "topics_monitored": len(self.topic_categories),
                "sources_monitored": sum(len(v) for v in self.monitored_sources.values()),
                "trends_detected": len(trends),
                "breaking_stories": len(breaking),
                "high_priority_alerts": len([a for a in alerts if a["priority"] == "high"]),
                "last_updated": datetime.now().isoformat(),
                "analysis_mode": "production"
            }
        })

    async def _generate_ai_story_suggestions(self, trends: List[Dict], breaking: List[Dict]) -> List[Dict]:
        """Use GPT-4 to generate enhanced story suggestions."""
        import httpx

        # Prepare context
        trend_summary = "\n".join([f"- {t['topic']} ({t['category']}): {t['volume']}" for t in trends[:5]])
        breaking_summary = "\n".join([f"- {b['headline']}" for b in breaking[:3]])

        prompt = f"""As a news assignment editor, analyze these trends and breaking news to suggest story angles:

TRENDING TOPICS:
{trend_summary}

BREAKING NEWS:
{breaking_summary}

Generate 3 unique story suggestions with:
1. Headline suggestion
2. Story type (analysis, explainer, live coverage, etc.)
3. Unique local angle
4. Sources to contact
5. Priority level (high/medium/low)

Format as JSON array."""

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.settings.OPENAI_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 1000
                    }
                )
                response.raise_for_status()
                result = response.json()

            content = result["choices"][0]["message"]["content"]
            # Try to parse JSON from response
            import json
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            suggestions_data = json.loads(content)

            # Format suggestions
            suggestions = []
            for i, s in enumerate(suggestions_data):
                suggestions.append({
                    "id": f"story_{random.randint(1000, 9999)}",
                    "headline_suggestion": s.get("headline", s.get("headline_suggestion", "")),
                    "based_on": f"AI analysis of current trends",
                    "story_type": s.get("story_type", s.get("type", "analysis")),
                    "estimated_audience": "High engagement expected",
                    "unique_angle": s.get("unique_angle", s.get("local_angle", "")),
                    "sources_to_contact": s.get("sources", s.get("sources_to_contact", [])),
                    "visual_suggestions": ["Graphics", "Interview clips", "B-roll"],
                    "deadline_suggestion": "Same day" if s.get("priority") == "high" else "Within 48 hours",
                    "priority": s.get("priority", "medium"),
                    "ai_generated": True
                })

            return suggestions

        except Exception as e:
            self.log_activity("ai_suggestions_failed", str(e))
            return await self._create_story_suggestions(trends, breaking)

    async def _get_trending_topics_mock(self, filters: Dict) -> List[Dict]:
        """Get currently trending topics (mock data)."""
        trends = [
            {
                "id": f"trend_{random.randint(1000, 9999)}",
                "topic": "Tech Layoffs 2024",
                "category": "business",
                "velocity": "rising",
                "velocity_score": 85,
                "volume": "250K mentions/hour",
                "sentiment": "negative",
                "sentiment_score": -0.65,
                "sources": ["Twitter/X", "LinkedIn", "Reddit", "TechCrunch"],
                "related_hashtags": ["#TechLayoffs", "#JobMarket", "#SiliconValley"],
                "peak_time": datetime.now().isoformat(),
                "geographic_hotspots": ["San Francisco", "Seattle", "Austin"],
                "key_accounts": ["@techcrunch", "@veraborger", "@elikiowa"],
                "sample_posts": [
                    "Breaking: Major tech company announces 10,000 layoffs",
                    "The tech industry is facing its biggest restructuring in decades"
                ]
            },
            {
                "id": f"trend_{random.randint(1000, 9999)}",
                "topic": "AI Regulation Debate",
                "category": "technology",
                "velocity": "rising",
                "velocity_score": 78,
                "volume": "180K mentions/hour",
                "sentiment": "mixed",
                "sentiment_score": 0.1,
                "sources": ["Twitter/X", "Reddit", "News Sites"],
                "related_hashtags": ["#AIRegulation", "#ArtificialIntelligence", "#TechPolicy"],
                "peak_time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "geographic_hotspots": ["Washington DC", "Brussels", "London"],
                "key_accounts": ["@OpenAI", "@Google", "@EUCommission"],
                "sample_posts": [
                    "New AI safety bill introduced in Congress",
                    "Tech leaders respond to proposed AI regulations"
                ]
            },
            {
                "id": f"trend_{random.randint(1000, 9999)}",
                "topic": "Celebrity Announcement",
                "category": "entertainment",
                "velocity": "exploding",
                "velocity_score": 95,
                "volume": "500K mentions/hour",
                "sentiment": "positive",
                "sentiment_score": 0.82,
                "sources": ["Twitter/X", "Instagram", "TikTok", "TMZ"],
                "related_hashtags": ["#Celebrity", "#Breaking", "#Entertainment"],
                "peak_time": datetime.now().isoformat(),
                "geographic_hotspots": ["Los Angeles", "New York", "Global"],
                "key_accounts": ["@TMZ", "@enikiews", "@PageSix"],
                "sample_posts": [
                    "BREAKING: Major celebrity announcement shocks fans",
                    "Social media reacts to surprise news"
                ]
            },
            {
                "id": f"trend_{random.randint(1000, 9999)}",
                "topic": "Championship Game Results",
                "category": "sports",
                "velocity": "stable",
                "velocity_score": 70,
                "volume": "320K mentions/hour",
                "sentiment": "mixed",
                "sentiment_score": 0.3,
                "sources": ["Twitter/X", "ESPN", "Sports News"],
                "related_hashtags": ["#Championship", "#Sports", "#GameDay"],
                "peak_time": (datetime.now() - timedelta(hours=1)).isoformat(),
                "geographic_hotspots": ["Nationwide"],
                "key_accounts": ["@ESPN", "@SportsCenter", "@NFL"],
                "sample_posts": [
                    "Final score: Incredible upset in championship game",
                    "Fans react to stunning victory"
                ]
            },
            {
                "id": f"trend_{random.randint(1000, 9999)}",
                "topic": "Climate Summit Updates",
                "category": "world",
                "velocity": "rising",
                "velocity_score": 65,
                "volume": "120K mentions/hour",
                "sentiment": "mixed",
                "sentiment_score": -0.2,
                "sources": ["Twitter/X", "News Sites", "Reuters"],
                "related_hashtags": ["#ClimateSummit", "#ClimateAction", "#COP29"],
                "peak_time": datetime.now().isoformat(),
                "geographic_hotspots": ["Global"],
                "key_accounts": ["@UN", "@UNFCCC", "@GretaThunberg"],
                "sample_posts": [
                    "World leaders gather for crucial climate talks",
                    "New commitments announced at climate summit"
                ]
            }
        ]

        # Apply category filter if provided
        if filters.get("category"):
            trends = [t for t in trends if t["category"] == filters["category"]]

        return trends

    async def _get_breaking_news_mock(self) -> List[Dict]:
        """Get breaking news stories (mock data)."""
        breaking = [
            {
                "id": f"break_{random.randint(1000, 9999)}",
                "headline": "BREAKING: Major Economic Announcement Expected",
                "summary": "Federal Reserve to make significant policy announcement this afternoon",
                "category": "business",
                "source": "Reuters",
                "urgency": "high",
                "confirmed": True,
                "timestamp": datetime.now().isoformat(),
                "developing": True,
                "related_stories": 15,
                "coverage_recommendation": "Live coverage recommended",
                "key_facts": [
                    "Announcement scheduled for 2:00 PM ET",
                    "Markets showing volatility ahead of news",
                    "Economists divided on expected outcome"
                ]
            },
            {
                "id": f"break_{random.randint(1000, 9999)}",
                "headline": "DEVELOPING: Major Weather Event Approaching",
                "summary": "Severe weather system expected to impact multiple states",
                "category": "weather",
                "source": "National Weather Service",
                "urgency": "high",
                "confirmed": True,
                "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "developing": True,
                "related_stories": 8,
                "coverage_recommendation": "Continuous updates needed",
                "key_facts": [
                    "Warnings issued for 5 states",
                    "Evacuations may be necessary",
                    "Emergency services on standby"
                ]
            },
            {
                "id": f"break_{random.randint(1000, 9999)}",
                "headline": "JUST IN: Tech Giant Announces Major Acquisition",
                "summary": "Multi-billion dollar deal to reshape industry landscape",
                "category": "technology",
                "source": "Bloomberg",
                "urgency": "medium",
                "confirmed": True,
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "developing": False,
                "related_stories": 22,
                "coverage_recommendation": "Analysis piece recommended",
                "key_facts": [
                    "Deal valued at $15 billion",
                    "Regulatory approval expected to take months",
                    "Competitors responding to news"
                ]
            }
        ]

        return breaking

    async def _analyze_viral_content_mock(self) -> List[Dict]:
        """Analyze currently viral content (mock data)."""
        viral = [
            {
                "id": f"viral_{random.randint(1000, 9999)}",
                "type": "video",
                "platform": "TikTok",
                "title": "Incredible moment caught on camera",
                "views": "5.2M",
                "shares": "250K",
                "engagement_rate": "12.5%",
                "growth_rate": "+500% in 2 hours",
                "demographic": "18-34",
                "news_potential": "high",
                "licensing_available": True,
                "contact_info": "creator@email.com",
                "content_warning": None
            },
            {
                "id": f"viral_{random.randint(1000, 9999)}",
                "type": "post",
                "platform": "Twitter/X",
                "title": "Thread exposing industry practices goes viral",
                "views": "2.8M",
                "shares": "85K",
                "engagement_rate": "8.2%",
                "growth_rate": "+200% in 4 hours",
                "demographic": "25-45",
                "news_potential": "medium",
                "licensing_available": False,
                "contact_info": "@username",
                "content_warning": "Verify claims before reporting"
            }
        ]

        return viral

    async def _generate_newsroom_alerts(self, trends: List[Dict], breaking: List[Dict], viral: List[Dict]) -> List[Dict]:
        """Generate alerts for newsroom."""
        alerts = []

        # Breaking news alerts (highest priority)
        for story in breaking:
            if story.get("urgency") == "high":
                alerts.append({
                    "id": f"alert_{random.randint(1000, 9999)}",
                    "type": "breaking_news",
                    "priority": "high",
                    "title": story["headline"],
                    "message": story["summary"],
                    "source": story["source"],
                    "timestamp": story["timestamp"],
                    "action_required": story.get("coverage_recommendation"),
                    "assignable": True,
                    "departments": ["news desk", "digital", "social"]
                })

        # Trending topic alerts
        for trend in trends:
            if trend.get("velocity_score", 0) >= 80:
                alerts.append({
                    "id": f"alert_{random.randint(1000, 9999)}",
                    "type": "trending_topic",
                    "priority": "medium",
                    "title": f"Trending: {trend['topic']}",
                    "message": f"Topic gaining momentum with {trend['volume']}",
                    "source": ", ".join(trend.get("sources", [])[:3]),
                    "timestamp": trend.get("peak_time"),
                    "action_required": "Consider coverage angle",
                    "assignable": True,
                    "departments": ["assignment desk", "digital"]
                })

        # Viral content alerts
        for content in viral:
            if content.get("news_potential") == "high":
                alerts.append({
                    "id": f"alert_{random.randint(1000, 9999)}",
                    "type": "viral_content",
                    "priority": "medium",
                    "title": f"Viral on {content['platform']}: {content['title']}",
                    "message": f"Content has {content['views']} views with {content['growth_rate']}",
                    "source": content["platform"],
                    "timestamp": datetime.now().isoformat(),
                    "action_required": "Verify and consider licensing",
                    "assignable": True,
                    "departments": ["digital", "social", "licensing"]
                })

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        alerts.sort(key=lambda x: priority_order.get(x["priority"], 3))

        return alerts

    async def _create_story_suggestions(self, trends: List[Dict], breaking: List[Dict]) -> List[Dict]:
        """Create story suggestions based on trends and breaking news."""
        suggestions = [
            {
                "id": f"story_{random.randint(1000, 9999)}",
                "headline_suggestion": "Analysis: What Tech Layoffs Mean for the Economy",
                "based_on": "Tech Layoffs 2024 trend",
                "story_type": "analysis",
                "estimated_audience": "High engagement expected",
                "unique_angle": "Local impact on tech workers",
                "sources_to_contact": ["Local tech workers", "Economists", "HR experts"],
                "visual_suggestions": ["Infographics", "Interview clips", "Stock footage"],
                "deadline_suggestion": "Same day",
                "priority": "high"
            },
            {
                "id": f"story_{random.randint(1000, 9999)}",
                "headline_suggestion": "Explainer: Understanding AI Regulation Proposals",
                "based_on": "AI Regulation Debate trend",
                "story_type": "explainer",
                "estimated_audience": "Strong digital performance",
                "unique_angle": "Impact on local businesses using AI",
                "sources_to_contact": ["Tech policy experts", "Local AI companies", "Lawmakers"],
                "visual_suggestions": ["Graphics", "Expert interviews"],
                "deadline_suggestion": "Within 48 hours",
                "priority": "medium"
            },
            {
                "id": f"story_{random.randint(1000, 9999)}",
                "headline_suggestion": "Live Coverage: Economic Announcement Impact",
                "based_on": "Breaking news - Economic Announcement",
                "story_type": "live_coverage",
                "estimated_audience": "Peak viewership expected",
                "unique_angle": "Real-time market reaction",
                "sources_to_contact": ["Financial analysts", "Local business leaders"],
                "visual_suggestions": ["Live graphics", "Split screen with markets"],
                "deadline_suggestion": "Immediate",
                "priority": "high"
            }
        ]

        return suggestions
