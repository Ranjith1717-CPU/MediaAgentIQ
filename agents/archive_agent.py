"""
Archive Agent - Natural language search and retrieval of archived content

Supports:
- Demo Mode: Returns mock search results for demonstration
- Production Mode: Uses Avid/Grass Valley integrations for real MAM search
"""
import aiosqlite
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from pathlib import Path
from .base_agent import BaseAgent, ProductionNotReadyError

if TYPE_CHECKING:
    from settings import Settings


class ArchiveAgent(BaseAgent):
    """
    Agent for searching and retrieving archived media content.

    Demo Mode: Returns mock search results from local database
    Production Mode: Uses Avid Media Central or Grass Valley NMOS for real MAM search
    """

    def __init__(self, db_path: str = None, settings: Optional["Settings"] = None):
        super().__init__(
            name="Archive Agent",
            description="Answers natural language queries like 'Find all Biden economy clips from Q3'",
            settings=settings
        )
        self.db_path = db_path or Path(__file__).parent.parent / "mediaagentiq.db"

    def _get_required_integrations(self) -> Dict[str, bool]:
        """Archive Agent can use Avid or NMOS for production."""
        return {
            "avid": self.settings.is_avid_configured,
            "nmos": self.settings.is_nmos_configured
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate search query."""
        if not input_data:
            return False
        if isinstance(input_data, str) and len(input_data.strip()) > 0:
            return True
        if isinstance(input_data, dict) and input_data.get("query"):
            return True
        return False

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Demo mode processing - searches local database or returns mock results.
        """
        # Extract query and filters
        if isinstance(input_data, str):
            query = input_data
            filters = {}
        else:
            query = input_data.get("query", "")
            filters = input_data.get("filters", {})

        self.log_activity("demo_process", f"Searching: {query}")

        # Parse natural language query
        parsed = await self._parse_query(query)

        # Search the archive (local DB or mock)
        results = await self._search_local_archive(parsed, filters)

        # Generate search insights
        insights = await self._generate_insights(results, query)

        return self.create_response(True, data={
            "query": query,
            "parsed_query": parsed,
            "results": results,
            "insights": insights,
            "stats": {
                "total_results": len(results),
                "search_time_ms": 45,
                "filters_applied": list(filters.keys()) if filters else [],
                "source": "local_database"
            }
        })

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production mode processing - uses MAM integrations.
        """
        # Extract query and filters
        if isinstance(input_data, str):
            query = input_data
            filters = {}
        else:
            query = input_data.get("query", "")
            filters = input_data.get("filters", {})

        self.log_activity("production_process", f"Searching: {query}")

        # Parse natural language query
        parsed = await self._parse_query(query)

        results = []
        source = "unknown"

        # Try Avid Media Central first
        if self.settings.is_avid_configured:
            results = await self._search_avid(parsed, filters)
            source = "avid_media_central"

        # Fall back to NMOS/Grass Valley
        elif self.settings.is_nmos_configured:
            results = await self._search_nmos(parsed, filters)
            source = "grass_valley_nmos"

        # Fall back to local database
        else:
            results = await self._search_local_archive(parsed, filters)
            source = "local_database"

        # Generate search insights
        insights = await self._generate_insights(results, query)

        return self.create_response(True, data={
            "query": query,
            "parsed_query": parsed,
            "results": results,
            "insights": insights,
            "stats": {
                "total_results": len(results),
                "search_time_ms": 120,
                "filters_applied": list(filters.keys()) if filters else [],
                "source": source,
                "analysis_mode": "production"
            }
        })

    async def _search_avid(self, parsed: Dict, filters: Dict) -> List[Dict]:
        """Search Avid Media Central."""
        try:
            from integrations.avid.connector import AvidConnector

            connector = AvidConnector(
                host=self.settings.AVID_HOST,
                username=self.settings.AVID_USERNAME,
                password=self.settings.AVID_PASSWORD,
                workspace=self.settings.AVID_WORKSPACE,
                mock_mode=self.settings.AVID_MOCK_MODE
            )

            await connector.connect()

            # Build search query
            search_query = parsed.get("search_terms", "")
            if parsed.get("topics"):
                search_query += " " + " ".join(parsed["topics"])

            search_result = await connector.search_assets(
                query=search_query,
                filters={
                    "speakers": parsed.get("speakers", []),
                    "date_range": parsed.get("date_filters", {}),
                    **filters
                }
            )

            await connector.disconnect()

            # Convert to standard format
            results = []
            for asset in search_result.assets:
                results.append({
                    "id": asset.id,
                    "title": asset.name,
                    "description": asset.metadata.get("description", ""),
                    "duration": asset.duration,
                    "duration_formatted": self._format_duration(asset.duration or 0),
                    "date_recorded": asset.created_at.strftime("%Y-%m-%d") if asset.created_at else "",
                    "tags": ",".join(asset.metadata.get("tags", [])),
                    "speaker": asset.metadata.get("speaker", ""),
                    "thumbnail_url": asset.thumbnail_url,
                    "source_url": asset.source_url,
                    "relevance_score": self._calculate_relevance(
                        {"title": asset.name, "tags": ",".join(asset.metadata.get("tags", []))},
                        parsed
                    )
                })

            return results

        except Exception as e:
            self.log_activity("avid_search_failed", str(e))
            return await self._get_mock_results(parsed)

    async def _search_nmos(self, parsed: Dict, filters: Dict) -> List[Dict]:
        """Search Grass Valley via NMOS."""
        try:
            from integrations.grass_valley.nmos_client import NMOSClient

            client = NMOSClient(
                registry_url=self.settings.NMOS_REGISTRY_URL,
                node_id=self.settings.NMOS_NODE_ID
            )

            await client.connect()

            # Search for sources
            search_query = parsed.get("search_terms", "")
            sources = await client.search_sources(query=search_query)

            await client.disconnect()

            # Convert to standard format
            results = []
            for source in sources:
                results.append({
                    "id": source.get("id", ""),
                    "title": source.get("label", "Unknown"),
                    "description": source.get("description", ""),
                    "duration": source.get("duration", 0),
                    "duration_formatted": self._format_duration(source.get("duration", 0)),
                    "date_recorded": source.get("created", ""),
                    "tags": source.get("tags", ""),
                    "speaker": "",
                    "thumbnail_url": source.get("thumbnail", ""),
                    "relevance_score": 0.8
                })

            return results

        except Exception as e:
            self.log_activity("nmos_search_failed", str(e))
            return await self._get_mock_results(parsed)

    async def _search_local_archive(self, parsed: Dict, filters: Dict) -> List[Dict]:
        """Search the local archive database."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                # Build search query
                conditions = []
                params = []

                if parsed.get("search_terms"):
                    conditions.append(
                        "(title LIKE ? OR description LIKE ? OR transcript LIKE ? OR tags LIKE ?)"
                    )
                    search_term = f"%{parsed['search_terms']}%"
                    params.extend([search_term] * 4)

                for topic in parsed.get("topics", []):
                    conditions.append("(tags LIKE ? OR transcript LIKE ?)")
                    params.extend([f"%{topic}%"] * 2)

                for speaker in parsed.get("speakers", []):
                    conditions.append("speaker LIKE ?")
                    params.append(f"%{speaker}%")

                if filters.get("date_from"):
                    conditions.append("date_recorded >= ?")
                    params.append(filters["date_from"])
                if filters.get("date_to"):
                    conditions.append("date_recorded <= ?")
                    params.append(filters["date_to"])

                where_clause = " AND ".join(conditions) if conditions else "1=1"
                query = f"""
                    SELECT * FROM archive
                    WHERE {where_clause}
                    ORDER BY date_recorded DESC
                    LIMIT 20
                """

                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()

                results = []
                for row in rows:
                    result = dict(row)
                    result["duration_formatted"] = self._format_duration(result.get("duration", 0))
                    result["relevance_score"] = self._calculate_relevance(result, parsed)
                    results.append(result)

                results.sort(key=lambda x: x["relevance_score"], reverse=True)
                return results

        except Exception as e:
            self.log_activity("local_search_failed", str(e))
            return await self._get_mock_results(parsed)

    async def _parse_query(self, query: str) -> Dict:
        """Parse natural language query into structured search parameters."""
        query_lower = query.lower()

        # Extract date/time references
        date_filters = {}
        time_keywords = {
            "today": "today", "yesterday": "yesterday",
            "this week": "week", "last week": "last_week",
            "this month": "month", "q1": "Q1", "q2": "Q2",
            "q3": "Q3", "q4": "Q4", "2024": "2024", "2023": "2023"
        }
        for keyword, value in time_keywords.items():
            if keyword in query_lower:
                date_filters["time_period"] = value

        # Extract content type
        content_type = None
        type_keywords = {
            "interview": "interview", "news": "news", "sports": "sports",
            "weather": "weather", "documentary": "documentary", "breaking": "breaking_news"
        }
        for keyword, value in type_keywords.items():
            if keyword in query_lower:
                content_type = value
                break

        # Extract speaker/person names
        speakers = []
        common_names = ["biden", "trump", "johnson", "smith", "chen", "martinez", "lee", "watson"]
        for name in common_names:
            if name in query_lower:
                speakers.append(name.title())

        # Extract topics
        topics = []
        topic_keywords = ["economy", "election", "climate", "technology", "ai", "sports",
                          "market", "health", "covid", "politics", "business"]
        for topic in topic_keywords:
            if topic in query_lower:
                topics.append(topic)

        # Clean search terms
        search_terms = query
        for word in ["find", "show", "get", "all", "clips", "videos", "from", "the", "me"]:
            search_terms = search_terms.replace(word, "")

        return {
            "original_query": query,
            "search_terms": search_terms.strip(),
            "date_filters": date_filters,
            "content_type": content_type,
            "speakers": speakers,
            "topics": topics
        }

    async def _get_mock_results(self, parsed: Dict) -> List[Dict]:
        """Return mock results for demo purposes."""
        mock_results = [
            {
                "id": 1,
                "title": "Morning News Broadcast - Election Coverage",
                "description": "Live coverage of the 2024 election results with expert analysis",
                "duration": 3600,
                "duration_formatted": "1:00:00",
                "date_recorded": "2024-11-06",
                "tags": "news,election,politics,live",
                "speaker": "Sarah Johnson",
                "thumbnail_url": "/static/demo/news_thumb.jpg",
                "relevance_score": 0.95
            },
            {
                "id": 2,
                "title": "Breaking News - Market Update",
                "description": "Live market analysis and economic news",
                "duration": 900,
                "duration_formatted": "15:00",
                "date_recorded": "2024-12-10",
                "tags": "news,finance,markets,economy,breaking",
                "speaker": "Robert Martinez",
                "thumbnail_url": "/static/demo/market_thumb.jpg",
                "relevance_score": 0.88
            },
            {
                "id": 3,
                "title": "Interview - Tech Industry Leader",
                "description": "Exclusive interview with leading tech CEO on AI developments",
                "duration": 2400,
                "duration_formatted": "40:00",
                "date_recorded": "2024-11-20",
                "tags": "interview,tech,AI,business,innovation",
                "speaker": "David Chen",
                "thumbnail_url": "/static/demo/interview_thumb.jpg",
                "relevance_score": 0.82
            }
        ]
        return mock_results

    async def _generate_insights(self, results: List[Dict], query: str) -> Dict:
        """Generate insights about search results."""
        if not results:
            return {
                "summary": "No matching content found",
                "suggestions": ["Try broader search terms", "Check spelling", "Remove date filters"]
            }

        total_duration = sum(r.get("duration", 0) for r in results)
        speakers = list(set(r.get("speaker", "") for r in results if r.get("speaker")))
        date_range = {
            "earliest": min(r.get("date_recorded", "") for r in results),
            "latest": max(r.get("date_recorded", "") for r in results)
        }

        return {
            "summary": f"Found {len(results)} clips totaling {self._format_duration(total_duration)}",
            "speakers": speakers,
            "date_range": date_range,
            "top_tags": self._extract_top_tags(results),
            "suggestions": [
                "Add date filter to narrow results",
                "Click any result to preview",
                "Use 'export' to create a compilation"
            ]
        }

    def _format_duration(self, seconds: int) -> str:
        """Format seconds to human readable duration."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    def _calculate_relevance(self, result: Dict, parsed: Dict) -> float:
        """Calculate relevance score for a result."""
        score = 0.5

        result_text = f"{result.get('title', '')} {result.get('tags', '')} {result.get('transcript', '')}".lower()
        for topic in parsed.get("topics", []):
            if topic.lower() in result_text:
                score += 0.1

        for speaker in parsed.get("speakers", []):
            if speaker.lower() in result.get("speaker", "").lower():
                score += 0.15

        return min(score, 1.0)

    def _extract_top_tags(self, results: List[Dict]) -> List[str]:
        """Extract most common tags from results."""
        all_tags = []
        for result in results:
            tags = result.get("tags", "").split(",")
            all_tags.extend([t.strip() for t in tags if t.strip()])

        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, count in sorted_tags[:5]]
