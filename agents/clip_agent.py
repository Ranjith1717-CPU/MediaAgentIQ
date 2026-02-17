"""
Clip Agent - Monitors live broadcasts, identifies viral moments, auto-creates social clips
"""
import random
from typing import Any, Dict, List
from pathlib import Path
from .base_agent import BaseAgent


class ClipAgent(BaseAgent):
    """Agent for detecting viral moments and generating social clips."""

    def __init__(self):
        super().__init__(
            name="Clip Agent",
            description="Monitors live broadcasts, identifies viral moments, auto-creates social clips with captions"
        )
        self.viral_indicators = [
            "breaking", "exclusive", "shocking", "incredible", "amazing",
            "unbelievable", "historic", "unprecedented", "viral", "trending"
        ]
        self.emotion_keywords = {
            "excitement": ["wow", "amazing", "incredible", "unbelievable", "yes"],
            "surprise": ["what", "oh my", "shocking", "unexpected", "breaking"],
            "inspiration": ["inspiring", "powerful", "moving", "emotional", "touching"],
            "humor": ["funny", "hilarious", "laugh", "joke", "comedy"]
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate input file."""
        if not input_data:
            return False
        file_path = Path(input_data) if isinstance(input_data, str) else input_data
        valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        return file_path.suffix.lower() in valid_extensions

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Analyze video and detect viral moments."""
        if not await self.validate_input(input_data):
            return self.create_response(False, error="Invalid video file format")

        # Analyze for viral moments (mock analysis)
        viral_moments = await self._detect_viral_moments()

        # Generate clip suggestions
        clips = await self._generate_clip_suggestions(viral_moments)

        # Generate social post suggestions
        social_posts = await self._generate_social_posts(clips)

        return self.create_response(True, data={
            "viral_moments": viral_moments,
            "suggested_clips": clips,
            "social_posts": social_posts,
            "stats": {
                "total_moments_detected": len(viral_moments),
                "clips_generated": len(clips),
                "platforms_ready": ["Twitter/X", "Instagram", "TikTok", "YouTube Shorts"],
                "estimated_reach": f"{random.randint(10, 100)}K - {random.randint(100, 500)}K"
            }
        })

    async def _detect_viral_moments(self) -> List[Dict]:
        """Detect viral moments in the video (mock data)."""
        moments = [
            {
                "id": 1,
                "start": 45.5,
                "end": 52.0,
                "type": "breaking_news",
                "emotion": "excitement",
                "score": 0.95,
                "transcript": "This is breaking news! We're getting reports of a major development...",
                "indicators": ["breaking", "major", "exclusive"],
                "thumbnail": "/static/demo/moment1.jpg"
            },
            {
                "id": 2,
                "start": 120.0,
                "end": 135.5,
                "type": "emotional_peak",
                "emotion": "inspiration",
                "score": 0.88,
                "transcript": "An incredible moment as the community comes together in support...",
                "indicators": ["incredible", "community", "support"],
                "thumbnail": "/static/demo/moment2.jpg"
            },
            {
                "id": 3,
                "start": 245.0,
                "end": 260.0,
                "type": "interview_highlight",
                "emotion": "surprise",
                "score": 0.92,
                "transcript": "I've never seen anything like this in my 30 years of experience...",
                "indicators": ["never seen", "unprecedented"],
                "thumbnail": "/static/demo/moment3.jpg"
            },
            {
                "id": 4,
                "start": 380.0,
                "end": 395.0,
                "type": "reaction_moment",
                "emotion": "excitement",
                "score": 0.85,
                "transcript": "The crowd goes wild! Absolutely electric atmosphere here...",
                "indicators": ["wild", "electric", "atmosphere"],
                "thumbnail": "/static/demo/moment4.jpg"
            },
            {
                "id": 5,
                "start": 510.0,
                "end": 530.0,
                "type": "key_quote",
                "emotion": "inspiration",
                "score": 0.90,
                "transcript": "This will change everything we know about the industry...",
                "indicators": ["change", "everything", "industry"],
                "thumbnail": "/static/demo/moment5.jpg"
            }
        ]
        return moments

    async def _generate_clip_suggestions(self, moments: List[Dict]) -> List[Dict]:
        """Generate clip suggestions from viral moments."""
        clips = []
        for moment in moments:
            # Determine optimal clip duration
            duration = moment["end"] - moment["start"]
            if duration < 15:
                # Extend clip to meet minimum
                buffer = (15 - duration) / 2
                start = max(0, moment["start"] - buffer)
                end = moment["end"] + buffer
            else:
                start = moment["start"]
                end = moment["end"]

            clip = {
                "id": f"clip_{moment['id']}",
                "moment_id": moment["id"],
                "start": start,
                "end": end,
                "duration": end - start,
                "title": self._generate_clip_title(moment),
                "description": moment["transcript"][:100] + "...",
                "viral_score": moment["score"],
                "emotion": moment["emotion"],
                "platforms": self._get_recommended_platforms(moment),
                "hashtags": self._generate_hashtags(moment),
                "thumbnail": moment.get("thumbnail"),
                "status": "ready",
                "format_versions": [
                    {"platform": "TikTok", "aspect": "9:16", "duration": "< 60s"},
                    {"platform": "Instagram Reels", "aspect": "9:16", "duration": "< 90s"},
                    {"platform": "Twitter/X", "aspect": "16:9", "duration": "< 140s"},
                    {"platform": "YouTube Shorts", "aspect": "9:16", "duration": "< 60s"}
                ]
            }
            clips.append(clip)

        # Sort by viral score
        clips.sort(key=lambda x: x["viral_score"], reverse=True)
        return clips

    async def _generate_social_posts(self, clips: List[Dict]) -> List[Dict]:
        """Generate social media post suggestions for clips."""
        posts = []
        for clip in clips[:3]:  # Top 3 clips
            posts.append({
                "clip_id": clip["id"],
                "platform": "Twitter/X",
                "text": f"🔴 {clip['title']}\n\n{clip['description']}\n\n{' '.join(clip['hashtags'][:5])}",
                "char_count": 280,
                "best_time": "9:00 AM EST"
            })
            posts.append({
                "clip_id": clip["id"],
                "platform": "Instagram",
                "text": f"{clip['title']}\n\n{clip['description']}\n\n.\n.\n.\n{' '.join(clip['hashtags'])}",
                "char_count": 2200,
                "best_time": "12:00 PM EST"
            })
            posts.append({
                "clip_id": clip["id"],
                "platform": "TikTok",
                "text": f"{clip['title']} {' '.join(clip['hashtags'][:3])}",
                "char_count": 150,
                "best_time": "7:00 PM EST"
            })
        return posts

    def _generate_clip_title(self, moment: Dict) -> str:
        """Generate a catchy title for a clip."""
        titles_by_type = {
            "breaking_news": "BREAKING: Major Development Unfolds Live",
            "emotional_peak": "Powerful Moment Captures Hearts",
            "interview_highlight": "Exclusive Interview: Must-See Quote",
            "reaction_moment": "Incredible Crowd Reaction",
            "key_quote": "Quote That's Going Viral"
        }
        return titles_by_type.get(moment.get("type", ""), "Trending Moment")

    def _get_recommended_platforms(self, moment: Dict) -> List[str]:
        """Get recommended platforms based on content type."""
        if moment.get("emotion") == "humor":
            return ["TikTok", "Instagram Reels", "Twitter/X"]
        elif moment.get("type") == "breaking_news":
            return ["Twitter/X", "Facebook", "YouTube"]
        else:
            return ["Twitter/X", "Instagram", "TikTok", "YouTube Shorts"]

    def _generate_hashtags(self, moment: Dict) -> List[str]:
        """Generate relevant hashtags for the moment."""
        base_hashtags = ["#Breaking", "#Viral", "#MustWatch", "#Trending"]
        emotion_hashtags = {
            "excitement": ["#Incredible", "#Amazing", "#WOW"],
            "surprise": ["#Shocking", "#Unexpected", "#BreakingNews"],
            "inspiration": ["#Inspiring", "#Powerful", "#Emotional"],
            "humor": ["#Funny", "#LOL", "#Comedy"]
        }
        hashtags = base_hashtags + emotion_hashtags.get(moment.get("emotion", ""), [])
        return hashtags[:8]
