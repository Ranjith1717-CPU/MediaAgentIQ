"""
Vision Service - OpenAI GPT-4V Integration

Provides video/image analysis for:
- Scene detection
- Content classification
- Viral moment detection
- Compliance checking
- Object/person recognition
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import base64
import logging
import asyncio
import httpx

logger = logging.getLogger(__name__)


@dataclass
class SceneAnalysis:
    """Analysis of a video scene or frame."""
    timestamp: float
    description: str
    emotions: List[str] = field(default_factory=list)
    objects: List[str] = field(default_factory=list)
    people_count: int = 0
    text_detected: List[str] = field(default_factory=list)
    confidence: float = 1.0
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "description": self.description,
            "emotions": self.emotions,
            "objects": self.objects,
            "people_count": self.people_count,
            "text_detected": self.text_detected,
            "confidence": self.confidence,
            "tags": self.tags
        }


@dataclass
class ViralMoment:
    """Detected potentially viral moment."""
    start_time: float
    end_time: float
    title: str
    description: str
    viral_score: float  # 0-1
    emotion: str
    reasoning: str
    suggested_hashtags: List[str] = field(default_factory=list)
    platforms: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start_time,
            "end": self.end_time,
            "title": self.title,
            "description": self.description,
            "viral_score": self.viral_score,
            "emotion": self.emotion,
            "reasoning": self.reasoning,
            "hashtags": self.suggested_hashtags,
            "platforms": self.platforms
        }


@dataclass
class ComplianceIssue:
    """Detected compliance concern."""
    timestamp: float
    issue_type: str  # "profanity", "violence", "adult_content", etc.
    severity: str  # "low", "medium", "high", "critical"
    description: str
    confidence: float
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "type": self.issue_type,
            "severity": self.severity,
            "description": self.description,
            "confidence": self.confidence,
            "recommendation": self.recommendation
        }


class VisionService(ABC):
    """Abstract base for vision services."""

    @abstractmethod
    async def analyze_image(
        self,
        image_path: str,
        prompt: str = None
    ) -> SceneAnalysis:
        """Analyze a single image."""
        pass

    @abstractmethod
    async def analyze_video_frames(
        self,
        frame_paths: List[str],
        prompt: str = None
    ) -> List[SceneAnalysis]:
        """Analyze video frames."""
        pass

    @abstractmethod
    async def detect_viral_moments(
        self,
        frame_analyses: List[SceneAnalysis],
        transcript: str = None
    ) -> List[ViralMoment]:
        """Detect potentially viral moments."""
        pass

    @abstractmethod
    async def check_compliance(
        self,
        frame_paths: List[str],
        transcript: str = None
    ) -> List[ComplianceIssue]:
        """Check for compliance issues."""
        pass


class GPT4VisionService(VisionService):
    """
    OpenAI GPT-4V vision analysis service.

    Uses GPT-4 Vision for:
    - Frame-by-frame video analysis
    - Scene understanding
    - Emotional moment detection
    - Content compliance checking
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-vision-preview",
        timeout: int = 60
    ):
        """
        Initialize GPT-4V service.

        Args:
            api_key: OpenAI API key
            model: GPT-4V model ID
            timeout: Request timeout
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self._base_url = "https://api.openai.com/v1"

    async def analyze_image(
        self,
        image_path: str,
        prompt: str = None,
        timestamp: float = 0
    ) -> SceneAnalysis:
        """
        Analyze a single image using GPT-4V.

        Args:
            image_path: Path to image file
            prompt: Custom analysis prompt
            timestamp: Video timestamp (if from video)

        Returns:
            SceneAnalysis result
        """
        # Encode image to base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        # Determine image type
        suffix = Path(image_path).suffix.lower()
        media_type = "image/jpeg" if suffix in [".jpg", ".jpeg"] else "image/png"

        default_prompt = """Analyze this video frame and provide:
1. A brief description of what's happening
2. Detected emotions (list)
3. Key objects visible (list)
4. Number of people visible
5. Any text visible in frame
6. Relevant tags for this content

Respond in JSON format with keys: description, emotions, objects, people_count, text, tags"""

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt or default_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{media_type};base64,{image_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            result = response.json()

        # Parse response
        content = result["choices"][0]["message"]["content"]
        try:
            import json
            data = json.loads(content)
        except json.JSONDecodeError:
            data = {"description": content}

        return SceneAnalysis(
            timestamp=timestamp,
            description=data.get("description", ""),
            emotions=data.get("emotions", []),
            objects=data.get("objects", []),
            people_count=data.get("people_count", 0),
            text_detected=data.get("text", []),
            tags=data.get("tags", [])
        )

    async def analyze_video_frames(
        self,
        frame_paths: List[str],
        prompt: str = None,
        frame_interval: float = 1.0
    ) -> List[SceneAnalysis]:
        """
        Analyze multiple video frames.

        Args:
            frame_paths: List of frame image paths
            prompt: Custom analysis prompt
            frame_interval: Time between frames in seconds

        Returns:
            List of SceneAnalysis results
        """
        analyses = []
        for i, path in enumerate(frame_paths):
            timestamp = i * frame_interval
            analysis = await self.analyze_image(path, prompt, timestamp)
            analyses.append(analysis)
        return analyses

    async def detect_viral_moments(
        self,
        frame_analyses: List[SceneAnalysis],
        transcript: str = None
    ) -> List[ViralMoment]:
        """
        Detect potentially viral moments from frame analyses.

        Uses GPT-4 to analyze patterns and identify high-engagement moments.
        """
        # Prepare context for GPT-4
        context = "Analyze these video scenes for viral potential:\n\n"
        for analysis in frame_analyses:
            context += f"[{analysis.timestamp}s] {analysis.description}\n"
            context += f"  Emotions: {', '.join(analysis.emotions)}\n"

        if transcript:
            context += f"\nTranscript excerpt: {transcript[:500]}\n"

        prompt = f"""{context}

Identify moments with high viral potential. For each, provide:
- Time range (start_time, end_time in seconds)
- Catchy title
- Description
- Viral score (0-1)
- Primary emotion
- Why it could go viral
- Suggested hashtags
- Best platforms

Respond in JSON format as a list of viral moments."""

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4-turbo-preview",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                }
            )
            response.raise_for_status()
            result = response.json()

        content = result["choices"][0]["message"]["content"]
        try:
            import json
            # Try to extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            data = json.loads(content)
        except (json.JSONDecodeError, IndexError):
            return []

        moments = []
        for m in data if isinstance(data, list) else []:
            moments.append(ViralMoment(
                start_time=m.get("start_time", 0),
                end_time=m.get("end_time", 0),
                title=m.get("title", ""),
                description=m.get("description", ""),
                viral_score=m.get("viral_score", 0.5),
                emotion=m.get("emotion", ""),
                reasoning=m.get("reasoning", m.get("why", "")),
                suggested_hashtags=m.get("hashtags", []),
                platforms=m.get("platforms", [])
            ))

        return moments

    async def check_compliance(
        self,
        frame_paths: List[str],
        transcript: str = None
    ) -> List[ComplianceIssue]:
        """
        Check frames for compliance issues.

        Detects:
        - Inappropriate content
        - Violence
        - Profanity (in text overlays)
        - Brand/logo issues
        """
        issues = []

        prompt = """Analyze this frame for broadcast compliance issues:
- Inappropriate or adult content
- Violence or disturbing imagery
- Offensive text or symbols
- Brand logos (may require clearance)
- Any content unsuitable for broadcast

If issues found, respond with JSON: {"issues": [{"type": "", "severity": "", "description": "", "recommendation": ""}]}
If no issues: {"issues": []}"""

        for i, path in enumerate(frame_paths):
            try:
                analysis = await self.analyze_image(path, prompt)
                # Parse for issues (simplified)
                if "inappropriate" in analysis.description.lower():
                    issues.append(ComplianceIssue(
                        timestamp=i * 1.0,
                        issue_type="content",
                        severity="medium",
                        description=analysis.description,
                        confidence=0.8,
                        recommendation="Review content before broadcast"
                    ))
            except Exception as e:
                logger.warning(f"Frame analysis failed: {e}")

        return issues


class MockVisionService(VisionService):
    """
    Mock vision service for demo mode.
    """

    async def analyze_image(
        self,
        image_path: str,
        prompt: str = None
    ) -> SceneAnalysis:
        await asyncio.sleep(0.3)
        return SceneAnalysis(
            timestamp=0,
            description="News anchor at desk delivering breaking news about warehouse fire",
            emotions=["concerned", "professional"],
            objects=["desk", "microphone", "monitor", "graphics"],
            people_count=1,
            text_detected=["BREAKING NEWS", "WAREHOUSE FIRE"],
            confidence=0.95,
            tags=["news", "broadcast", "breaking", "fire"]
        )

    async def analyze_video_frames(
        self,
        frame_paths: List[str],
        prompt: str = None
    ) -> List[SceneAnalysis]:
        analyses = []
        scenes = [
            ("Anchor introduces breaking news", ["serious"]),
            ("Cut to live reporter at scene", ["urgent"]),
            ("Wide shot of fire and emergency vehicles", ["dramatic"]),
            ("Close-up of firefighters working", ["action"]),
            ("Reporter interview with witness", ["emotional"]),
        ]

        for i, path in enumerate(frame_paths):
            scene = scenes[i % len(scenes)]
            analyses.append(SceneAnalysis(
                timestamp=i * 5.0,
                description=scene[0],
                emotions=scene[1],
                objects=["camera", "equipment"],
                people_count=2,
                confidence=0.9,
                tags=["news", "breaking"]
            ))
            await asyncio.sleep(0.1)

        return analyses

    async def detect_viral_moments(
        self,
        frame_analyses: List[SceneAnalysis],
        transcript: str = None
    ) -> List[ViralMoment]:
        await asyncio.sleep(0.5)
        return [
            ViralMoment(
                start_time=145.0,
                end_time=162.0,
                title="Reporter's Close Call with Debris",
                description="Live reporter narrowly dodges falling debris during fire coverage",
                viral_score=0.97,
                emotion="shock",
                reasoning="Dramatic near-miss moments tend to go viral",
                suggested_hashtags=["#Breaking", "#CloseCall", "#LiveTV"],
                platforms=["TikTok", "Twitter", "Instagram"]
            ),
            ViralMoment(
                start_time=892.0,
                end_time=918.0,
                title="Emotional Family Reunion",
                description="Family reunited with pet after disaster",
                viral_score=0.95,
                emotion="heartwarming",
                reasoning="Emotional reunion content performs well across platforms",
                suggested_hashtags=["#Heartwarming", "#GoodNews", "#Miracle"],
                platforms=["Facebook", "Instagram", "TikTok"]
            )
        ]

    async def check_compliance(
        self,
        frame_paths: List[str],
        transcript: str = None
    ) -> List[ComplianceIssue]:
        await asyncio.sleep(0.3)
        return [
            ComplianceIssue(
                timestamp=125.5,
                issue_type="profanity",
                severity="high",
                description="Potential profanity detected in interview",
                confidence=0.85,
                recommendation="Review audio and consider bleeping"
            )
        ]
