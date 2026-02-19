"""
Transcription Service - OpenAI Whisper Integration

Provides speech-to-text transcription with:
- Speaker diarization (when available)
- Timestamp alignment
- Multi-language support
- Confidence scoring
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import logging
import asyncio
import httpx

logger = logging.getLogger(__name__)


@dataclass
class TranscriptSegment:
    """A segment of transcribed speech."""
    start: float  # Start time in seconds
    end: float  # End time in seconds
    text: str
    speaker: Optional[str] = None
    confidence: float = 1.0
    language: str = "en"
    words: List[Dict] = field(default_factory=list)  # Word-level timing

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "speaker": self.speaker,
            "confidence": self.confidence,
            "language": self.language,
            "words": self.words
        }


@dataclass
class TranscriptionResult:
    """Complete transcription result."""
    segments: List[TranscriptSegment]
    language: str
    duration: float
    text: str  # Full transcript text
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "segments": [s.to_dict() for s in self.segments],
            "language": self.language,
            "duration": self.duration,
            "text": self.text,
            "metadata": self.metadata
        }

    def to_srt(self) -> str:
        """Generate SRT format."""
        srt_lines = []
        for i, segment in enumerate(self.segments, 1):
            start = _format_srt_time(segment.start)
            end = _format_srt_time(segment.end)
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start} --> {end}")
            srt_lines.append(segment.text)
            srt_lines.append("")
        return "\n".join(srt_lines)

    def to_vtt(self) -> str:
        """Generate WebVTT format."""
        vtt_lines = ["WEBVTT", ""]
        for i, segment in enumerate(self.segments, 1):
            start = _format_vtt_time(segment.start)
            end = _format_vtt_time(segment.end)
            vtt_lines.append(f"{i}")
            vtt_lines.append(f"{start} --> {end}")
            vtt_lines.append(segment.text)
            vtt_lines.append("")
        return "\n".join(vtt_lines)


def _format_srt_time(seconds: float) -> str:
    """Format seconds to SRT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def _format_vtt_time(seconds: float) -> str:
    """Format seconds to VTT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


class TranscriptionService(ABC):
    """Abstract base for transcription services."""

    @abstractmethod
    async def transcribe(
        self,
        file_path: str,
        language: str = None,
        **kwargs
    ) -> TranscriptionResult:
        """
        Transcribe audio/video file.

        Args:
            file_path: Path to media file
            language: Optional language code (auto-detect if None)
            **kwargs: Service-specific options

        Returns:
            TranscriptionResult with segments
        """
        pass

    @abstractmethod
    async def transcribe_url(
        self,
        url: str,
        language: str = None,
        **kwargs
    ) -> TranscriptionResult:
        """
        Transcribe from URL.

        Args:
            url: URL to media file
            language: Optional language code
            **kwargs: Service-specific options

        Returns:
            TranscriptionResult
        """
        pass


class WhisperService(TranscriptionService):
    """
    OpenAI Whisper transcription service.

    Uses OpenAI's Whisper API for high-quality transcription.

    Features:
    - Multi-language support (50+ languages)
    - Automatic language detection
    - Word-level timestamps
    - Segment-level timestamps
    """

    def __init__(
        self,
        api_key: str,
        model: str = "whisper-1",
        timeout: int = 300
    ):
        """
        Initialize Whisper service.

        Args:
            api_key: OpenAI API key
            model: Whisper model ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self._base_url = "https://api.openai.com/v1"

    async def transcribe(
        self,
        file_path: str,
        language: str = None,
        response_format: str = "verbose_json",
        **kwargs
    ) -> TranscriptionResult:
        """
        Transcribe audio/video file using Whisper.

        Args:
            file_path: Path to media file
            language: Language code (e.g., "en", "es")
            response_format: Output format
            **kwargs: Additional options

        Returns:
            TranscriptionResult
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info(f"Transcribing with Whisper: {path.name}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with open(path, "rb") as f:
                files = {"file": (path.name, f, "audio/mpeg")}
                data = {
                    "model": self.model,
                    "response_format": response_format,
                    "timestamp_granularities[]": "segment"
                }

                if language:
                    data["language"] = language

                response = await client.post(
                    f"{self._base_url}/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files=files,
                    data=data
                )

                response.raise_for_status()
                result = response.json()

        return self._parse_response(result)

    async def transcribe_url(
        self,
        url: str,
        language: str = None,
        **kwargs
    ) -> TranscriptionResult:
        """
        Transcribe from URL.

        Note: Whisper API doesn't support URLs directly,
        so we download the file first.
        """
        import tempfile

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            # Save to temp file
            with tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            ) as f:
                f.write(response.content)
                temp_path = f.name

        try:
            return await self.transcribe(temp_path, language, **kwargs)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def _parse_response(self, response: Dict) -> TranscriptionResult:
        """Parse Whisper API response."""
        segments = []

        # Parse segments from verbose_json response
        for seg in response.get("segments", []):
            segments.append(TranscriptSegment(
                start=seg.get("start", 0),
                end=seg.get("end", 0),
                text=seg.get("text", "").strip(),
                confidence=seg.get("avg_logprob", 0) + 1,  # Convert logprob
                language=response.get("language", "en"),
                words=seg.get("words", [])
            ))

        # If no segments, create single segment from text
        if not segments and response.get("text"):
            segments.append(TranscriptSegment(
                start=0,
                end=response.get("duration", 0),
                text=response.get("text", "").strip(),
                language=response.get("language", "en")
            ))

        duration = response.get("duration", 0)
        if segments and not duration:
            duration = segments[-1].end

        return TranscriptionResult(
            segments=segments,
            language=response.get("language", "en"),
            duration=duration,
            text=response.get("text", ""),
            metadata={
                "model": self.model,
                "task": response.get("task", "transcribe")
            }
        )


class MockTranscriptionService(TranscriptionService):
    """
    Mock transcription for demo mode.

    Returns realistic mock data without API calls.
    """

    async def transcribe(
        self,
        file_path: str,
        language: str = None,
        **kwargs
    ) -> TranscriptionResult:
        """Return mock transcription."""
        # Simulate processing time
        await asyncio.sleep(1)

        mock_segments = [
            TranscriptSegment(0.0, 4.2, "Good morning, I'm Sarah Mitchell, and this is WKRN Morning News.", "Anchor", 0.99),
            TranscriptSegment(4.5, 9.8, "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.", "Anchor", 0.98),
            TranscriptSegment(10.2, 15.5, "Fire crews responded around 2 AM and battled the blaze for nearly four hours.", "Anchor", 0.97),
            TranscriptSegment(16.0, 20.3, "We go live now to reporter Jake Thompson at the scene. Jake, what's the latest?", "Anchor", 0.98),
            TranscriptSegment(21.0, 27.5, "Sarah, as you can see behind me, crews are still working to contain hot spots.", "Reporter", 0.96),
            TranscriptSegment(28.0, 34.2, "The warehouse, owned by Mitchell Distribution, stored electronics and furniture.", "Reporter", 0.94),
            TranscriptSegment(34.8, 41.0, "Fire Chief Robert Anderson told me moments ago that the cause is under investigation.", "Reporter", 0.97),
            TranscriptSegment(41.5, 48.3, "You can hear additional units arriving now to assist with the operation.", "Reporter", 0.89),
            TranscriptSegment(49.0, 55.8, "Thankfully, no injuries have been reported. The building was unoccupied at the time.", "Reporter", 0.98),
            TranscriptSegment(56.2, 62.0, "We'll have more updates throughout the morning. Back to you, Sarah.", "Reporter", 0.97),
        ]

        full_text = " ".join(s.text for s in mock_segments)

        return TranscriptionResult(
            segments=mock_segments,
            language=language or "en",
            duration=62.0,
            text=full_text,
            metadata={"mock": True}
        )

    async def transcribe_url(
        self,
        url: str,
        language: str = None,
        **kwargs
    ) -> TranscriptionResult:
        return await self.transcribe("mock_file.mp3", language, **kwargs)
