"""
Caption Agent - Auto-captioning and QA for media content
"""
import random
from typing import Any, Dict, List
from pathlib import Path
from .base_agent import BaseAgent


class CaptionAgent(BaseAgent):
    """Agent for generating and QA-checking captions."""

    def __init__(self):
        super().__init__(
            name="Caption Agent",
            description="Automatically generate captions with QA checks"
        )
        self.profanity_list = ["damn", "hell", "crap"]  # Demo list

    async def validate_input(self, input_data: Any) -> bool:
        """Validate that input is a valid media file path."""
        if not input_data:
            return False
        file_path = Path(input_data) if isinstance(input_data, str) else input_data
        valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".mp3", ".wav", ".m4a"}
        return file_path.suffix.lower() in valid_extensions

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Generate captions for the input media file."""
        if not await self.validate_input(input_data):
            return self.create_response(False, error="Invalid input file format")

        # Generate mock captions (in production, would use Whisper API)
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
                "qa_issues": len([r for r in qa_results if r["type"] == "warning" or r["type"] == "error"])
            }
        })

    async def _generate_mock_captions(self) -> List[Dict]:
        """Generate mock caption data for demo purposes."""
        mock_transcript = [
            {"start": 0.0, "end": 3.5, "text": "Welcome to today's broadcast.", "speaker": "Host", "confidence": 0.98},
            {"start": 3.5, "end": 7.2, "text": "We have an exciting show lined up for you.", "speaker": "Host", "confidence": 0.95},
            {"start": 7.5, "end": 12.0, "text": "Let's start with the top stories of the day.", "speaker": "Host", "confidence": 0.97},
            {"start": 12.5, "end": 18.0, "text": "Our first story covers the recent developments in technology.", "speaker": "Host", "confidence": 0.94},
            {"start": 18.5, "end": 24.0, "text": "Artificial intelligence continues to transform industries worldwide.", "speaker": "Host", "confidence": 0.96},
            {"start": 24.5, "end": 30.0, "text": "Experts predict significant changes in the coming years.", "speaker": "Host", "confidence": 0.93},
            {"start": 30.5, "end": 36.0, "text": "Now let's hear from our correspondent in the field.", "speaker": "Host", "confidence": 0.97},
            {"start": 36.5, "end": 42.0, "text": "Thank you. I'm here at the conference center.", "speaker": "Reporter", "confidence": 0.95},
            {"start": 42.5, "end": 48.0, "text": "Industry leaders are gathered to discuss the future.", "speaker": "Reporter", "confidence": 0.94},
            {"start": 48.5, "end": 54.0, "text": "The atmosphere here is electric with anticipation.", "speaker": "Reporter", "confidence": 0.92},
            {"start": 54.5, "end": 60.0, "text": "Back to you in the studio.", "speaker": "Reporter", "confidence": 0.98},
        ]
        return mock_transcript

    async def _run_qa_checks(self, captions: List[Dict]) -> List[Dict]:
        """Run quality assurance checks on captions."""
        issues = []

        for i, caption in enumerate(captions):
            # Check confidence threshold
            if caption.get("confidence", 1.0) < 0.90:
                issues.append({
                    "type": "warning",
                    "segment": i + 1,
                    "timestamp": self.format_timestamp(caption["start"]),
                    "issue": "Low confidence score",
                    "details": f"Confidence: {caption.get('confidence', 0):.2%}",
                    "suggestion": "Review and verify this segment manually"
                })

            # Check for profanity
            text_lower = caption["text"].lower()
            for word in self.profanity_list:
                if word in text_lower:
                    issues.append({
                        "type": "error",
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
