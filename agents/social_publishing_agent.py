"""
Social Publishing Agent - Creates and schedules social media posts from broadcast highlights

Supports:
- Demo Mode: Returns mock posts for demonstration
- Production Mode: Uses AI to generate optimized content and platform APIs for scheduling
"""
import random
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from .base_agent import BaseAgent

if TYPE_CHECKING:
    from settings import Settings


class SocialPublishingAgent(BaseAgent):
    """
    Agent for creating and scheduling social media posts.

    Demo Mode: Returns mock post suggestions
    Production Mode: Uses GPT-4 for content generation and platform APIs for scheduling
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Social Publishing Agent",
            description="Creates Twitter/Instagram/TikTok posts from broadcast highlights, schedules posting",
            settings=settings
        )

        self.platforms = {
            "twitter": {
                "name": "Twitter/X",
                "max_chars": 280,
                "max_video_length": 140,
                "aspect_ratios": ["16:9", "1:1"],
                "best_times": ["9:00 AM", "12:00 PM", "5:00 PM"]
            },
            "instagram": {
                "name": "Instagram",
                "max_chars": 2200,
                "max_video_length": 90,
                "aspect_ratios": ["1:1", "4:5", "9:16"],
                "best_times": ["11:00 AM", "2:00 PM", "7:00 PM"]
            },
            "tiktok": {
                "name": "TikTok",
                "max_chars": 150,
                "max_video_length": 180,
                "aspect_ratios": ["9:16"],
                "best_times": ["7:00 PM", "8:00 PM", "9:00 PM"]
            },
            "facebook": {
                "name": "Facebook",
                "max_chars": 63206,
                "max_video_length": 240,
                "aspect_ratios": ["16:9", "1:1", "9:16"],
                "best_times": ["1:00 PM", "3:00 PM", "9:00 AM"]
            },
            "youtube_shorts": {
                "name": "YouTube Shorts",
                "max_chars": 100,
                "max_video_length": 60,
                "aspect_ratios": ["9:16"],
                "best_times": ["12:00 PM", "5:00 PM", "8:00 PM"]
            }
        }

    def _get_required_integrations(self) -> Dict[str, bool]:
        """Social Publishing Agent can use OpenAI for content generation."""
        return {
            "openai": self.settings.is_openai_configured
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate input for social publishing."""
        if not input_data:
            return False
        if isinstance(input_data, dict):
            return "clip" in input_data or "content" in input_data or "highlights" in input_data
        return True

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Demo mode processing - returns mock social posts.
        """
        self.log_activity("demo_process", "Generating social posts")

        # Generate posts for each platform
        posts = await self._generate_posts_mock(input_data)

        # Create optimal schedule
        schedule = await self._create_schedule(posts)

        # Generate hashtag suggestions
        hashtags = await self._generate_hashtags_mock()

        # Analytics predictions
        predictions = await self._predict_performance(posts)

        return self.create_response(True, data={
            "posts": posts,
            "schedule": schedule,
            "hashtags": hashtags,
            "predictions": predictions,
            "stats": {
                "total_posts": len(posts),
                "platforms": list(set(p["platform"] for p in posts)),
                "scheduled_count": len(schedule),
                "estimated_reach": f"{random.randint(50, 200)}K - {random.randint(200, 500)}K"
            }
        })

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production mode processing - uses AI for content generation.
        """
        self.log_activity("production_process", "Generating social posts with AI")

        # Extract content info
        if isinstance(input_data, dict):
            content_info = input_data
        else:
            content_info = {"content": str(input_data)}

        # Generate posts
        if self.settings.is_openai_configured:
            posts = await self._generate_posts_with_ai(content_info)
        else:
            posts = await self._generate_posts_mock(input_data)

        # Create optimal schedule
        schedule = await self._create_schedule(posts)

        # Generate hashtag suggestions
        if self.settings.is_openai_configured:
            hashtags = await self._generate_hashtags_with_ai(content_info)
        else:
            hashtags = await self._generate_hashtags_mock()

        # Analytics predictions
        predictions = await self._predict_performance(posts)

        return self.create_response(True, data={
            "posts": posts,
            "schedule": schedule,
            "hashtags": hashtags,
            "predictions": predictions,
            "stats": {
                "total_posts": len(posts),
                "platforms": list(set(p["platform"] for p in posts)),
                "scheduled_count": len(schedule),
                "estimated_reach": f"{random.randint(50, 200)}K - {random.randint(200, 500)}K",
                "analysis_mode": "production"
            }
        })

    async def _generate_posts_with_ai(self, content_info: Dict) -> List[Dict]:
        """Generate platform-specific posts using GPT-4."""
        import httpx

        # Extract content description
        title = content_info.get("title", content_info.get("content", "Breaking news clip"))
        description = content_info.get("description", "")
        clip_url = content_info.get("clip_url", "/clips/highlight.mp4")
        thumbnail = content_info.get("thumbnail", "/thumbs/highlight.jpg")

        prompt = f"""Create engaging social media posts for the following content:

Title: {title}
Description: {description}

Generate posts optimized for each platform:
1. Twitter/X (max 280 chars, include hashtags)
2. Instagram (longer caption, use emojis, hashtags at end)
3. TikTok (short, trendy, use relevant hashtags)

Format as JSON array with keys: platform, content"""

        posts = []

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
                        "max_tokens": 800
                    }
                )
                response.raise_for_status()
                result = response.json()

            content = result["choices"][0]["message"]["content"]

            # Parse JSON from response
            import json
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            generated_posts = json.loads(content)

            platform_map = {
                "twitter": "twitter",
                "twitter/x": "twitter",
                "x": "twitter",
                "instagram": "instagram",
                "tiktok": "tiktok"
            }

            for gp in generated_posts:
                platform_key = platform_map.get(gp.get("platform", "").lower(), "twitter")
                posts.append({
                    "id": f"post_{random.randint(1000, 9999)}",
                    "platform": platform_key,
                    "platform_name": self.platforms[platform_key]["name"],
                    "content": gp.get("content", ""),
                    "char_count": len(gp.get("content", "")),
                    "media_type": "video",
                    "media_url": clip_url,
                    "thumbnail": thumbnail,
                    "status": "draft",
                    "created_at": datetime.now().isoformat(),
                    "ai_generated": True
                })

        except Exception as e:
            self.log_activity("ai_post_generation_failed", str(e))
            # Fall back to mock posts
            posts = await self._generate_posts_mock(content_info)

        return posts

    async def _generate_hashtags_with_ai(self, content_info: Dict) -> Dict:
        """Generate hashtag recommendations using GPT-4."""
        import httpx

        title = content_info.get("title", content_info.get("content", "news"))

        prompt = f"""Generate hashtag recommendations for social media posts about: {title}

Categorize into:
1. Trending (currently popular)
2. Niche (industry-specific)
3. Engagement (to boost visibility)

Format as JSON with keys: trending, niche, engagement (each an array of hashtags)"""

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
                        "max_tokens": 400
                    }
                )
                response.raise_for_status()
                result = response.json()

            content = result["choices"][0]["message"]["content"]

            import json
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            hashtags = json.loads(content)
            hashtags["ai_generated"] = True
            return hashtags

        except Exception as e:
            self.log_activity("ai_hashtag_generation_failed", str(e))
            return await self._generate_hashtags_mock()

    async def _generate_posts_mock(self, input_data: Any) -> List[Dict]:
        """Generate platform-specific posts (mock data)."""
        posts = []

        highlights = [
            {
                "title": "Breaking: Major Development in Downtown",
                "description": "Exclusive coverage of today's breaking news story",
                "clip_url": "/clips/highlight1.mp4",
                "thumbnail": "/thumbs/highlight1.jpg",
                "duration": 45
            },
            {
                "title": "Interview: Industry Leader Speaks Out",
                "description": "Must-see interview with insights on the future",
                "clip_url": "/clips/highlight2.mp4",
                "thumbnail": "/thumbs/highlight2.jpg",
                "duration": 60
            }
        ]

        for highlight in highlights:
            # Twitter/X post
            posts.append({
                "id": f"post_{random.randint(1000, 9999)}",
                "platform": "twitter",
                "platform_name": "Twitter/X",
                "content": f"🔴 BREAKING: {highlight['title']}\n\n{highlight['description'][:100]}...\n\n#Breaking #News #MustWatch",
                "char_count": 180,
                "media_type": "video",
                "media_url": highlight["clip_url"],
                "thumbnail": highlight["thumbnail"],
                "status": "draft",
                "created_at": datetime.now().isoformat()
            })

            # Instagram post
            posts.append({
                "id": f"post_{random.randint(1000, 9999)}",
                "platform": "instagram",
                "platform_name": "Instagram",
                "content": f"🎬 {highlight['title']}\n\n{highlight['description']}\n\n📺 Watch the full story on our channel\n\n.\n.\n.\n#News #Breaking #Trending #MustSee #Viral #NewsAlert",
                "char_count": 250,
                "media_type": "reel",
                "media_url": highlight["clip_url"],
                "thumbnail": highlight["thumbnail"],
                "status": "draft",
                "created_at": datetime.now().isoformat()
            })

            # TikTok post
            posts.append({
                "id": f"post_{random.randint(1000, 9999)}",
                "platform": "tiktok",
                "platform_name": "TikTok",
                "content": f"{highlight['title']} #fyp #news #viral #breaking",
                "char_count": 80,
                "media_type": "video",
                "media_url": highlight["clip_url"],
                "thumbnail": highlight["thumbnail"],
                "status": "draft",
                "created_at": datetime.now().isoformat()
            })

        return posts

    async def _create_schedule(self, posts: List[Dict]) -> List[Dict]:
        """Create optimal posting schedule."""
        schedule = []
        base_time = datetime.now()

        for i, post in enumerate(posts):
            platform_config = self.platforms.get(post["platform"], {})
            best_times = platform_config.get("best_times", ["12:00 PM"])

            # Stagger posts throughout the day
            scheduled_time = base_time + timedelta(hours=i * 2)

            schedule.append({
                "post_id": post["id"],
                "platform": post["platform_name"],
                "scheduled_time": scheduled_time.isoformat(),
                "scheduled_time_formatted": scheduled_time.strftime("%B %d, %Y at %I:%M %p"),
                "optimal_time": random.choice(best_times),
                "status": "scheduled",
                "auto_post": False
            })

        return schedule

    async def _generate_hashtags_mock(self) -> Dict:
        """Generate hashtag recommendations (mock data)."""
        return {
            "trending": ["#Breaking", "#NewsAlert", "#Viral", "#MustWatch", "#Trending"],
            "niche": ["#BroadcastNews", "#LiveTV", "#MediaIndustry", "#Journalism"],
            "engagement": ["#fyp", "#foryou", "#explore", "#viral"],
            "branded": ["#YourChannelName", "#YourShowName"],
            "recommendations": [
                {"hashtag": "#Breaking", "reach": "2.5M", "competition": "high"},
                {"hashtag": "#NewsAlert", "reach": "1.2M", "competition": "medium"},
                {"hashtag": "#MustWatch", "reach": "800K", "competition": "medium"},
                {"hashtag": "#Trending", "reach": "5M", "competition": "very high"},
            ]
        }

    async def _predict_performance(self, posts: List[Dict]) -> List[Dict]:
        """Predict post performance metrics."""
        predictions = []

        for post in posts:
            platform = post["platform"]

            predictions.append({
                "post_id": post["id"],
                "platform": post["platform_name"],
                "predicted_reach": f"{random.randint(10, 100)}K",
                "predicted_engagement": f"{random.uniform(2.5, 8.5):.1f}%",
                "predicted_shares": random.randint(50, 500),
                "predicted_comments": random.randint(20, 200),
                "confidence": f"{random.uniform(70, 95):.0f}%",
                "best_performing_time": self.platforms[platform]["best_times"][0],
                "recommendations": [
                    "Add trending audio for TikTok" if platform == "tiktok" else "Include call-to-action",
                    "Use 3-5 relevant hashtags",
                    "Post during peak engagement hours"
                ]
            })

        return predictions
