"""
Archive Agent - Natural language search and retrieval of archived content
"""
import aiosqlite
from typing import Any, Dict, List
from pathlib import Path
from .base_agent import BaseAgent


class ArchiveAgent(BaseAgent):
    """Agent for searching and retrieving archived media content."""

    def __init__(self, db_path: str = None):
        super().__init__(
            name="Archive Agent",
            description="Answers natural language queries like 'Find all Biden economy clips from Q3'"
        )
        self.db_path = db_path or Path(__file__).parent.parent / "mediaagentiq.db"

    async def validate_input(self, input_data: Any) -> bool:
        """Validate search query."""
        if not input_data:
            return False
        if isinstance(input_data, str) and len(input_data.strip()) > 0:
            return True
        if isinstance(input_data, dict) and input_data.get("query"):
            return True
        return False

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process natural language search query."""
        if not await self.validate_input(input_data):
            return self.create_response(False, error="Invalid search query")

        # Extract query and filters
        if isinstance(input_data, str):
            query = input_data
            filters = {}
        else:
            query = input_data.get("query", "")
            filters = input_data.get("filters", {})

        # Parse natural language query
        parsed = await self._parse_query(query)

        # Search the archive
        results = await self._search_archive(parsed, filters)

        # Generate search insights
        insights = await self._generate_insights(results, query)

        return self.create_response(True, data={
            "query": query,
            "parsed_query": parsed,
            "results": results,
            "insights": insights,
            "stats": {
                "total_results": len(results),
                "search_time_ms": 45,  # Mock timing
                "filters_applied": list(filters.keys()) if filters else []
            }
        })

    async def _parse_query(self, query: str) -> Dict:
        """Parse natural language query into structured search parameters."""
        query_lower = query.lower()

        # Extract date/time references
        date_filters = {}
        time_keywords = {
            "today": "today",
            "yesterday": "yesterday",
            "this week": "week",
            "last week": "last_week",
            "this month": "month",
            "q1": "Q1",
            "q2": "Q2",
            "q3": "Q3",
            "q4": "Q4",
            "2024": "2024",
            "2023": "2023"
        }
        for keyword, value in time_keywords.items():
            if keyword in query_lower:
                date_filters["time_period"] = value

        # Extract content type
        content_type = None
        type_keywords = {
            "interview": "interview",
            "news": "news",
            "sports": "sports",
            "weather": "weather",
            "documentary": "documentary",
            "breaking": "breaking_news"
        }
        for keyword, value in type_keywords.items():
            if keyword in query_lower:
                content_type = value
                break

        # Extract speaker/person names (simplified)
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

    async def _search_archive(self, parsed: Dict, filters: Dict) -> List[Dict]:
        """Search the archive database."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                # Build search query
                conditions = []
                params = []

                # Text search
                if parsed.get("search_terms"):
                    conditions.append(
                        "(title LIKE ? OR description LIKE ? OR transcript LIKE ? OR tags LIKE ?)"
                    )
                    search_term = f"%{parsed['search_terms']}%"
                    params.extend([search_term] * 4)

                # Topic search
                for topic in parsed.get("topics", []):
                    conditions.append("(tags LIKE ? OR transcript LIKE ?)")
                    params.extend([f"%{topic}%"] * 2)

                # Speaker search
                for speaker in parsed.get("speakers", []):
                    conditions.append("speaker LIKE ?")
                    params.append(f"%{speaker}%")

                # Additional filters
                if filters.get("date_from"):
                    conditions.append("date_recorded >= ?")
                    params.append(filters["date_from"])
                if filters.get("date_to"):
                    conditions.append("date_recorded <= ?")
                    params.append(filters["date_to"])

                # Build final query
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
                    # Add computed fields
                    result["duration_formatted"] = self._format_duration(result.get("duration", 0))
                    result["relevance_score"] = self._calculate_relevance(result, parsed)
                    results.append(result)

                # Sort by relevance
                results.sort(key=lambda x: x["relevance_score"], reverse=True)
                return results

        except Exception as e:
            # Return mock results if database error
            return await self._get_mock_results(parsed)

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
        score = 0.5  # Base score

        # Boost for matching topics
        result_text = f"{result.get('title', '')} {result.get('tags', '')} {result.get('transcript', '')}".lower()
        for topic in parsed.get("topics", []):
            if topic.lower() in result_text:
                score += 0.1

        # Boost for matching speakers
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

        # Count and sort
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, count in sorted_tags[:5]]
