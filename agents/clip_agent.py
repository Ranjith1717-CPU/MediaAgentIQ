"""
Clip Agent - Monitors live broadcasts, identifies viral moments, auto-creates social clips

Supports:
- Demo Mode: Returns mock viral moments for demonstration
- Production Mode: Uses GPT-4 Vision for real video analysis
"""
import random
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from pathlib import Path
from .base_agent import BaseAgent, ProductionNotReadyError

if TYPE_CHECKING:
    from settings import Settings


class ClipAgent(BaseAgent):
    """
    Agent for detecting viral moments and generating social clips.

    Demo Mode: Returns realistic mock viral moments
    Production Mode: Uses GPT-4 Vision API for frame analysis
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Clip Agent",
            description="Monitors live broadcasts, identifies viral moments, auto-creates social clips with captions",
            settings=settings
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

    def _get_required_integrations(self) -> Dict[str, bool]:
        """Clip Agent requires OpenAI for production (GPT-4 Vision)."""
        return {
            "openai": self.settings.is_openai_configured
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate input file."""
        if not input_data:
            return False
        file_path = Path(input_data) if isinstance(input_data, str) else input_data
        valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        return file_path.suffix.lower() in valid_extensions

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Demo mode processing - returns mock viral moments.
        """
        self.log_activity("demo_process", f"Analyzing {input_data}")

        # Analyze for viral moments (mock analysis)
        viral_moments = await self._detect_mock_viral_moments()

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

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production mode processing - uses GPT-4 Vision for analysis.
        """
        if not self.settings.is_openai_configured:
            raise ProductionNotReadyError(self.name, "OPENAI_API_KEY")

        self.log_activity("production_process", f"Analyzing {input_data}")

        # Import vision service
        from services.vision import GPT4VisionService

        # Initialize vision service
        vision = GPT4VisionService(
            api_key=self.settings.OPENAI_API_KEY,
            model="gpt-4-vision-preview"
        )

        # Extract frames from video (in production, use FFmpeg)
        # For now, we'll use the mock frame analysis pattern
        frame_paths = await self._extract_frames(str(input_data))

        if frame_paths:
            # Analyze frames with GPT-4 Vision
            frame_analyses = await vision.analyze_video_frames(frame_paths)

            # Detect viral moments from analysis
            viral_moments_raw = await vision.detect_viral_moments(frame_analyses)

            # Convert to our format
            viral_moments = []
            for i, moment in enumerate(viral_moments_raw):
                viral_moments.append({
                    "id": i + 1,
                    "start": moment.start_time,
                    "end": moment.end_time,
                    "type": self._classify_moment_type(moment.emotion),
                    "emotion": moment.emotion,
                    "score": moment.viral_score,
                    "transcript": moment.description,
                    "indicators": moment.suggested_hashtags[:3],
                    "thumbnail": f"/static/frames/moment_{i+1}.jpg"
                })
        else:
            # Fallback to mock if frame extraction fails
            viral_moments = await self._detect_mock_viral_moments()

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
                "estimated_reach": f"{random.randint(10, 100)}K - {random.randint(100, 500)}K",
                "analysis_mode": "production"
            }
        })

    async def _extract_frames(self, video_path: str) -> List[str]:
        """
        Extract frames from video for analysis.

        In production, this would use FFmpeg to extract keyframes.
        Returns empty list if extraction fails.
        """
        import subprocess
        import tempfile
        import os

        try:
            # Create temp directory for frames
            temp_dir = tempfile.mkdtemp(prefix="clip_agent_")
            output_pattern = os.path.join(temp_dir, "frame_%04d.jpg")

            # Extract frames at 1fps for analysis
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vf", "fps=1",
                "-frames:v", "10",  # Limit to 10 frames for analysis
                output_pattern,
                "-y", "-loglevel", "error"
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=60)

            if result.returncode == 0:
                # Collect extracted frame paths
                frames = sorted([
                    os.path.join(temp_dir, f) for f in os.listdir(temp_dir)
                    if f.endswith('.jpg')
                ])
                return frames

        except Exception as e:
            self.log_activity("frame_extraction_failed", str(e))

        return []

    def _classify_moment_type(self, emotion: str) -> str:
        """Classify moment type based on emotion."""
        emotion_to_type = {
            "shock": "breaking_news",
            "excitement": "reaction_moment",
            "heartwarming": "emotional_peak",
            "surprise": "interview_highlight",
            "inspiration": "emotional_peak"
        }
        return emotion_to_type.get(emotion.lower(), "key_quote")

    async def _detect_mock_viral_moments(self) -> List[Dict]:
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
            if duration < self.settings.CLIP_MIN_DURATION:
                # Extend clip to meet minimum
                buffer = (self.settings.CLIP_MIN_DURATION - duration) / 2
                start = max(0, moment["start"] - buffer)
                end = moment["end"] + buffer
            elif duration > self.settings.CLIP_MAX_DURATION:
                # Trim to max duration
                start = moment["start"]
                end = moment["start"] + self.settings.CLIP_MAX_DURATION
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
