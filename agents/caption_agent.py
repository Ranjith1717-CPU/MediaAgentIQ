"""
Caption Agent - Auto-captioning and QA for media content

Supports:
- Demo Mode: Returns mock captions for demonstration
- Production Mode: Uses OpenAI Whisper for real transcription
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from pathlib import Path
import logging

from .base_agent import BaseAgent, ProductionNotReadyError

if TYPE_CHECKING:
    from settings import Settings

logger = logging.getLogger(__name__)


class CaptionAgent(BaseAgent):
    """
    Agent for generating and QA-checking captions.

    Demo Mode: Returns realistic mock captions
    Production Mode: Uses OpenAI Whisper API for transcription
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Caption Agent",
            description="Automatically generate captions with QA checks",
            settings=settings
        )
        self.profanity_list = ["damn", "hell", "crap", "ass", "bastard"]

    def _get_required_integrations(self) -> Dict[str, bool]:
        """Caption Agent requires OpenAI for production."""
        return {
            "openai": self.settings.is_openai_configured
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate that input is a valid media file path."""
        if not input_data:
            return False
        file_path = Path(input_data) if isinstance(input_data, str) else input_data
        valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".mp3", ".wav", ".m4a"}
        return file_path.suffix.lower() in valid_extensions

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Demo mode processing - returns mock captions.
        """
        self.log_activity("demo_process", f"Processing {input_data}")

        # Generate mock captions
        captions = await self._generate_mock_captions()

        # Run QA checks
        qa_results = await self._run_qa_checks(captions)

        # Generate output formats
        srt_content = self._generate_srt(captions)
        vtt_content = self._generate_vtt(captions)

        return self.create_response(True, data={
            "captions": captions,
            "qa_results": qa_results,
            "srt": srt_content,
            "vtt": vtt_content,
            "stats": {
                "total_segments": len(captions),
                "total_duration": captions[-1]["end"] if captions else 0,
                "word_count": sum(len(c["text"].split()) for c in captions),
                "qa_issues": len([r for r in qa_results if r["type"] in ("warning", "error")])
            }
        })

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production mode processing - uses OpenAI Whisper API.
        """
        if not self.settings.is_openai_configured:
            raise ProductionNotReadyError(self.name, "OPENAI_API_KEY")

        self.log_activity("production_process", f"Transcribing {input_data}")

        # Import transcription service
        from services.transcription import WhisperService

        # Initialize Whisper service
        whisper = WhisperService(
            api_key=self.settings.OPENAI_API_KEY,
            model=self.settings.OPENAI_WHISPER_MODEL
        )

        # Transcribe
        result = await whisper.transcribe(str(input_data))

        # Convert to caption format
        captions = []
        for segment in result.segments:
            captions.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "speaker": segment.speaker or "Speaker",
                "confidence": segment.confidence
            })

        # Run QA checks
        qa_results = await self._run_qa_checks(captions)

        # Generate output formats
        srt_content = result.to_srt()
        vtt_content = result.to_vtt()

        return self.create_response(True, data={
            "captions": captions,
            "qa_results": qa_results,
            "srt": srt_content,
            "vtt": vtt_content,
            "stats": {
                "total_segments": len(captions),
                "total_duration": result.duration,
                "word_count": len(result.text.split()),
                "qa_issues": len([r for r in qa_results if r["type"] in ("warning", "error")]),
                "language": result.language
            }
        })

    async def _generate_mock_captions(self) -> List[Dict]:
        """Generate mock caption data for demo purposes."""
        mock_transcript = [
            {"start": 0.0, "end": 4.2, "text": "Good morning, I'm Sarah Mitchell, and this is WKRN Morning News.", "speaker": "Anchor", "confidence": 0.99},
            {"start": 4.5, "end": 9.8, "text": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.", "speaker": "Anchor", "confidence": 0.98},
            {"start": 10.2, "end": 15.5, "text": "Fire crews responded around 2 AM and battled the blaze for nearly four hours.", "speaker": "Anchor", "confidence": 0.97},
            {"start": 16.0, "end": 20.3, "text": "We go live now to reporter Jake Thompson at the scene. Jake, what's the latest?", "speaker": "Anchor", "confidence": 0.98},
            {"start": 21.0, "end": 27.5, "text": "Sarah, as you can see behind me, crews are still working to contain hot spots.", "speaker": "Reporter", "confidence": 0.96},
            {"start": 28.0, "end": 34.2, "text": "The warehouse, owned by Mitchell Distribution, stored electronics and furniture.", "speaker": "Reporter", "confidence": 0.94},
            {"start": 34.8, "end": 41.0, "text": "Fire Chief Robert Anderson told me moments ago that the cause is under investigation.", "speaker": "Reporter", "confidence": 0.97},
            {"start": 41.5, "end": 48.3, "text": "You can hear additional units arriving now to assist with the operation.", "speaker": "Reporter", "confidence": 0.89},
            {"start": 49.0, "end": 55.8, "text": "Thankfully, no injuries have been reported. The building was unoccupied at the time.", "speaker": "Reporter", "confidence": 0.98},
            {"start": 56.2, "end": 62.0, "text": "We'll have more updates throughout the morning. Back to you, Sarah.", "speaker": "Reporter", "confidence": 0.97},
            {"start": 62.5, "end": 68.4, "text": "Thank you, Jake. Stay safe out there. We'll check back with you at the top of the hour.", "speaker": "Anchor", "confidence": 0.98},
        ]
        return mock_transcript

    async def _run_qa_checks(self, captions: List[Dict]) -> List[Dict]:
        """Run quality assurance checks on captions."""
        issues = []

        for i, caption in enumerate(captions):
            # Check confidence threshold
            confidence = caption.get("confidence", 1.0)
            if confidence < self.settings.CAPTION_CONFIDENCE_THRESHOLD:
                issues.append({
                    "type": "warning",
                    "severity": "medium",
                    "segment": i + 1,
                    "timestamp": self.format_timestamp(caption["start"]),
                    "issue": "Low confidence score",
                    "details": f"Confidence: {confidence:.0%}",
                    "suggestion": "Review and verify this segment manually"
                })

            # Check for profanity
            text_lower = caption["text"].lower()
            for word in self.profanity_list:
                if word in text_lower:
                    issues.append({
                        "type": "error",
                        "severity": "high",
                        "segment": i + 1,
                        "timestamp": self.format_timestamp(caption["start"]),
                        "issue": "Potential profanity detected",
                        "details": f"Found: '{word}'",
                        "suggestion": "Consider censoring or removing"
                    })

            # Check timing gaps
            if i > 0:
                gap = caption["start"] - captions[i - 1]["end"]
                if gap > 3.0:
                    issues.append({
                        "type": "info",
                        "severity": "low",
                        "segment": i + 1,
                        "timestamp": self.format_timestamp(caption["start"]),
                        "issue": "Large gap between segments",
                        "details": f"Gap: {gap:.1f} seconds",
                        "suggestion": "Verify no content is missing"
                    })

            # Check segment duration
            duration = caption["end"] - caption["start"]
            if duration > 7.0:
                issues.append({
                    "type": "warning",
                    "severity": "medium",
                    "segment": i + 1,
                    "timestamp": self.format_timestamp(caption["start"]),
                    "issue": "Long segment duration",
                    "details": f"Duration: {duration:.1f} seconds",
                    "suggestion": "Consider splitting into smaller segments"
                })

            # Check for speaker changes
            if i > 0 and caption.get("speaker") != captions[i - 1].get("speaker"):
                issues.append({
                    "type": "info",
                    "severity": "low",
                    "segment": i + 1,
                    "timestamp": self.format_timestamp(caption["start"]),
                    "issue": "Speaker change detected",
                    "details": f"New speaker: {caption.get('speaker', 'Unknown')}",
                    "suggestion": "Verify speaker identification"
                })

        # Add overall assessment
        if not issues:
            issues.append({
                "type": "success",
                "severity": "none",
                "segment": None,
                "timestamp": None,
                "issue": "All checks passed",
                "details": "No issues found in caption quality",
                "suggestion": None
            })

        return issues

    def _generate_srt(self, captions: List[Dict]) -> str:
        """Generate SRT format captions."""
        srt_lines = []
        for i, caption in enumerate(captions, 1):
            start_time = self.format_timestamp(caption["start"])
            end_time = self.format_timestamp(caption["end"])
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(caption["text"])
            srt_lines.append("")
        return "\n".join(srt_lines)

    def _generate_vtt(self, captions: List[Dict]) -> str:
        """Generate WebVTT format captions."""
        vtt_lines = ["WEBVTT", ""]
        for i, caption in enumerate(captions, 1):
            start_time = self.format_vtt_timestamp(caption["start"])
            end_time = self.format_vtt_timestamp(caption["end"])
            vtt_lines.append(f"{i}")
            vtt_lines.append(f"{start_time} --> {end_time}")
            vtt_lines.append(caption["text"])
            vtt_lines.append("")
        return "\n".join(vtt_lines)
