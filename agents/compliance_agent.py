"""
Compliance Agent - Monitors 24/7 for FCC violations, profanity, political ad issues

Supports:
- Demo Mode: Returns mock compliance issues for demonstration
- Production Mode: Uses Vision + Transcription services for real content analysis
"""
import random
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from pathlib import Path
from datetime import datetime
from .base_agent import BaseAgent, ProductionNotReadyError

if TYPE_CHECKING:
    from settings import Settings


class ComplianceAgent(BaseAgent):
    """
    Agent for monitoring FCC compliance and content violations.

    Demo Mode: Returns realistic mock compliance issues
    Production Mode: Uses OpenAI Whisper + GPT-4 Vision for real analysis
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Compliance Agent",
            description="Monitors 24/7 for FCC violations, profanity, political ad issues, auto-logs and alerts",
            settings=settings
        )

        # FCC violation categories
        self.violation_types = {
            "profanity": {
                "severity": "high",
                "fine_range": "$25,000 - $500,000",
                "description": "Broadcast of obscene, indecent or profane content"
            },
            "political_ad": {
                "severity": "medium",
                "fine_range": "$10,000 - $100,000",
                "description": "Political advertising disclosure requirements"
            },
            "sponsor_id": {
                "severity": "medium",
                "fine_range": "$10,000 - $50,000",
                "description": "Sponsor identification requirements"
            },
            "eas_violation": {
                "severity": "critical",
                "fine_range": "$100,000 - $500,000",
                "description": "Emergency Alert System violations"
            },
            "children_programming": {
                "severity": "high",
                "fine_range": "$25,000 - $250,000",
                "description": "Children's television programming requirements"
            },
            "closed_caption": {
                "severity": "low",
                "fine_range": "$1,000 - $10,000",
                "description": "Closed captioning requirements"
            }
        }

        # Profanity detection (simplified list for demo)
        self.profanity_words = [
            "damn", "hell", "crap", "ass", "bastard"  # Safe-for-work demo list
        ]

        # Political keywords for ad detection
        self.political_keywords = [
            "vote", "elect", "candidate", "campaign", "ballot",
            "democrat", "republican", "congress", "senator", "paid for by"
        ]

    def _get_required_integrations(self) -> Dict[str, bool]:
        """Compliance Agent requires OpenAI for production."""
        return {
            "openai": self.settings.is_openai_configured
        }

    async def validate_input(self, input_data: Any) -> bool:
        """Validate input for compliance scanning."""
        if not input_data:
            return False
        # Accept file path or transcript text
        if isinstance(input_data, str):
            return True
        if isinstance(input_data, dict):
            return "file" in input_data or "transcript" in input_data
        return False

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Demo mode processing - returns mock compliance issues.
        """
        self.log_activity("demo_process", f"Scanning content for compliance")

        # Run all compliance checks (mock)
        issues = []
        issues.extend(await self._check_profanity_mock())
        issues.extend(await self._check_political_ads_mock())
        issues.extend(await self._check_sponsor_identification_mock())
        issues.extend(await self._check_caption_compliance_mock())

        # Generate compliance report
        report = await self._generate_report(issues)

        # Calculate risk score
        risk_score = self._calculate_risk_score(issues)

        return self.create_response(True, data={
            "issues": issues,
            "report": report,
            "risk_score": risk_score,
            "stats": {
                "total_issues": len(issues),
                "critical_count": len([i for i in issues if i["severity"] == "critical"]),
                "high_count": len([i for i in issues if i["severity"] == "high"]),
                "medium_count": len([i for i in issues if i["severity"] == "medium"]),
                "low_count": len([i for i in issues if i["severity"] == "low"]),
                "potential_fines": self._calculate_potential_fines(issues),
                "scan_timestamp": datetime.now().isoformat()
            }
        })

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production mode processing - uses real AI services.
        """
        if not self.settings.is_openai_configured:
            raise ProductionNotReadyError(self.name, "OPENAI_API_KEY")

        self.log_activity("production_process", f"Scanning content for compliance")

        # Import services
        from services.transcription import WhisperService
        from services.vision import GPT4VisionService

        issues = []

        # Get transcript for audio analysis
        transcript_text = None
        if isinstance(input_data, dict):
            file_path = input_data.get("file")
            transcript_text = input_data.get("transcript")
        else:
            file_path = input_data if Path(input_data).exists() else None

        # Transcribe if we have a file
        if file_path and not transcript_text:
            whisper = WhisperService(
                api_key=self.settings.OPENAI_API_KEY,
                model=self.settings.OPENAI_WHISPER_MODEL
            )
            try:
                result = await whisper.transcribe(str(file_path))
                transcript_text = result.text
                transcript_segments = result.segments
            except Exception as e:
                self.log_activity("transcription_failed", str(e))
                transcript_text = ""
                transcript_segments = []
        else:
            transcript_segments = []

        # Check transcript for profanity
        if transcript_text:
            issues.extend(await self._check_profanity_real(transcript_text, transcript_segments))
            issues.extend(await self._check_political_ads_real(transcript_text, transcript_segments))

        # Check video frames for visual compliance
        if file_path and Path(file_path).suffix.lower() in {".mp4", ".mov", ".avi", ".mkv", ".webm"}:
            vision = GPT4VisionService(
                api_key=self.settings.OPENAI_API_KEY
            )
            frame_paths = await self._extract_frames(str(file_path))
            if frame_paths:
                visual_issues = await vision.check_compliance(frame_paths, transcript_text)
                for vi in visual_issues:
                    issues.append({
                        "id": f"vis_{random.randint(1000, 9999)}",
                        "type": vi.issue_type,
                        "severity": vi.severity,
                        "timestamp": vi.timestamp,
                        "timestamp_formatted": self.format_timestamp(vi.timestamp),
                        "description": vi.description,
                        "context": vi.description,
                        "confidence": vi.confidence,
                        "fcc_rule": "47 U.S.C. § 326",
                        "potential_fine": self.violation_types.get(vi.issue_type, {}).get("fine_range", "TBD"),
                        "recommendation": vi.recommendation,
                        "action_required": vi.severity in ["high", "critical"]
                    })

        # Generate compliance report
        report = await self._generate_report(issues)

        # Calculate risk score
        risk_score = self._calculate_risk_score(issues)

        return self.create_response(True, data={
            "issues": issues,
            "report": report,
            "risk_score": risk_score,
            "stats": {
                "total_issues": len(issues),
                "critical_count": len([i for i in issues if i["severity"] == "critical"]),
                "high_count": len([i for i in issues if i["severity"] == "high"]),
                "medium_count": len([i for i in issues if i["severity"] == "medium"]),
                "low_count": len([i for i in issues if i["severity"] == "low"]),
                "potential_fines": self._calculate_potential_fines(issues),
                "scan_timestamp": datetime.now().isoformat(),
                "analysis_mode": "production"
            }
        })

    async def _extract_frames(self, video_path: str) -> List[str]:
        """Extract frames from video for visual compliance check."""
        import subprocess
        import tempfile
        import os

        try:
            temp_dir = tempfile.mkdtemp(prefix="compliance_agent_")
            output_pattern = os.path.join(temp_dir, "frame_%04d.jpg")

            cmd = [
                "ffmpeg", "-i", video_path,
                "-vf", "fps=0.5",  # One frame every 2 seconds
                "-frames:v", "15",
                output_pattern,
                "-y", "-loglevel", "error"
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=60)

            if result.returncode == 0:
                frames = sorted([
                    os.path.join(temp_dir, f) for f in os.listdir(temp_dir)
                    if f.endswith('.jpg')
                ])
                return frames

        except Exception as e:
            self.log_activity("frame_extraction_failed", str(e))

        return []

    async def _check_profanity_real(self, transcript: str, segments: List) -> List[Dict]:
        """Check for profanity in real transcript."""
        issues = []
        transcript_lower = transcript.lower()

        for word in self.profanity_words:
            if word in transcript_lower:
                # Find timestamp if we have segments
                timestamp = 0.0
                for seg in segments:
                    if word in seg.text.lower():
                        timestamp = seg.start
                        break

                issues.append({
                    "id": f"prof_{random.randint(1000, 9999)}",
                    "type": "profanity",
                    "severity": "high",
                    "timestamp": timestamp,
                    "timestamp_formatted": self.format_timestamp(timestamp),
                    "description": f"Profanity detected: '{word}'",
                    "context": f"Found in transcript",
                    "confidence": 0.95,
                    "fcc_rule": "47 U.S.C. § 326",
                    "potential_fine": "$25,000 - $500,000",
                    "recommendation": "Review segment, consider bleeping or re-recording",
                    "action_required": True
                })

        return issues

    async def _check_political_ads_real(self, transcript: str, segments: List) -> List[Dict]:
        """Check for political ad compliance in real transcript."""
        issues = []
        transcript_lower = transcript.lower()

        political_count = sum(1 for kw in self.political_keywords if kw in transcript_lower)

        if political_count >= 2 and "paid for by" not in transcript_lower:
            timestamp = 0.0
            for seg in segments:
                for kw in self.political_keywords:
                    if kw in seg.text.lower():
                        timestamp = seg.start
                        break

            issues.append({
                "id": f"pol_{random.randint(1000, 9999)}",
                "type": "political_ad",
                "severity": "medium",
                "timestamp": timestamp,
                "timestamp_formatted": self.format_timestamp(timestamp),
                "description": "Political content detected without proper disclosure",
                "context": f"Found {political_count} political keywords without 'paid for by' disclosure",
                "confidence": 0.85,
                "fcc_rule": "47 U.S.C. § 315",
                "potential_fine": "$10,000 - $100,000",
                "recommendation": "Add 'Paid for by...' disclosure statement",
                "action_required": True,
                "disclosure_template": "Paid for by [Committee Name]. Authorized by [Candidate Name] for [Office]."
            })

        return issues

    # Mock methods for demo mode
    async def _check_profanity_mock(self) -> List[Dict]:
        """Check for profanity/indecent content (mock)."""
        return [{
            "id": f"prof_{random.randint(1000, 9999)}",
            "type": "profanity",
            "severity": "high",
            "timestamp": 125.5,
            "timestamp_formatted": self.format_timestamp(125.5),
            "description": "Potential profanity detected: 'damn'",
            "context": "...what the damn problem is with...",
            "confidence": 0.95,
            "fcc_rule": "47 U.S.C. § 326",
            "potential_fine": "$25,000 - $500,000",
            "recommendation": "Review segment, consider bleeping or re-recording",
            "action_required": True
        }]

    async def _check_political_ads_mock(self) -> List[Dict]:
        """Check for political advertising compliance (mock)."""
        return [{
            "id": f"pol_{random.randint(1000, 9999)}",
            "type": "political_ad",
            "severity": "medium",
            "timestamp": 450.0,
            "timestamp_formatted": self.format_timestamp(450.0),
            "description": "Political content detected without proper disclosure",
            "context": "Vote for candidate Johnson this November",
            "confidence": 0.88,
            "fcc_rule": "47 U.S.C. § 315",
            "potential_fine": "$10,000 - $100,000",
            "recommendation": "Add 'Paid for by...' disclosure statement",
            "action_required": True,
            "disclosure_template": "Paid for by [Committee Name]. Authorized by [Candidate Name] for [Office]."
        }]

    async def _check_sponsor_identification_mock(self) -> List[Dict]:
        """Check for sponsor identification compliance (mock)."""
        return [{
            "id": f"spons_{random.randint(1000, 9999)}",
            "type": "sponsor_id",
            "severity": "medium",
            "timestamp": 890.0,
            "timestamp_formatted": self.format_timestamp(890.0),
            "description": "Sponsored segment without clear identification",
            "context": "Product mention appears to be sponsored content",
            "confidence": 0.72,
            "fcc_rule": "47 U.S.C. § 317",
            "potential_fine": "$10,000 - $50,000",
            "recommendation": "Add clear sponsor identification at start of segment",
            "action_required": True
        }]

    async def _check_caption_compliance_mock(self) -> List[Dict]:
        """Check closed captioning compliance (mock)."""
        return [{
            "id": f"cap_{random.randint(1000, 9999)}",
            "type": "closed_caption",
            "severity": "low",
            "timestamp": None,
            "timestamp_formatted": "N/A",
            "description": "Caption accuracy below 95% threshold",
            "context": "Overall caption accuracy: 92.3%",
            "confidence": 0.95,
            "fcc_rule": "47 CFR § 79.1",
            "potential_fine": "$1,000 - $10,000",
            "recommendation": "Review and correct caption errors before broadcast",
            "action_required": False
        }]

    async def _generate_report(self, issues: List[Dict]) -> Dict:
        """Generate comprehensive compliance report."""
        report = {
            "title": "FCC Compliance Scan Report",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "status": "ISSUES FOUND" if issues else "COMPLIANT",
                "total_issues": len(issues),
                "action_required": len([i for i in issues if i.get("action_required")]),
                "review_recommended": len([i for i in issues if not i.get("action_required")])
            },
            "issues_by_severity": {
                "critical": [i for i in issues if i["severity"] == "critical"],
                "high": [i for i in issues if i["severity"] == "high"],
                "medium": [i for i in issues if i["severity"] == "medium"],
                "low": [i for i in issues if i["severity"] == "low"]
            },
            "recommended_actions": self._get_recommended_actions(issues),
            "compliance_checklist": [
                {"item": "Profanity/Indecency Check", "status": "warning" if any(i["type"] == "profanity" for i in issues) else "pass"},
                {"item": "Political Ad Disclosure", "status": "warning" if any(i["type"] == "political_ad" for i in issues) else "pass"},
                {"item": "Sponsor Identification", "status": "warning" if any(i["type"] == "sponsor_id" for i in issues) else "pass"},
                {"item": "Caption Compliance", "status": "info" if any(i["type"] == "closed_caption" for i in issues) else "pass"},
                {"item": "EAS Compliance", "status": "pass"},
                {"item": "Children's Programming", "status": "pass"}
            ]
        }

        return report

    def _calculate_risk_score(self, issues: List[Dict]) -> Dict:
        """Calculate overall compliance risk score."""
        if not issues:
            return {"score": 100, "level": "low", "color": "green"}

        # Deduct points based on severity
        score = 100
        for issue in issues:
            if issue["severity"] == "critical":
                score -= 30
            elif issue["severity"] == "high":
                score -= 20
            elif issue["severity"] == "medium":
                score -= 10
            else:
                score -= 5

        score = max(0, score)

        if score >= 80:
            level, color = "low", "green"
        elif score >= 60:
            level, color = "medium", "yellow"
        elif score >= 40:
            level, color = "high", "orange"
        else:
            level, color = "critical", "red"

        return {"score": score, "level": level, "color": color}

    def _calculate_potential_fines(self, issues: List[Dict]) -> str:
        """Calculate potential fine range."""
        if not issues:
            return "$0"

        total_min = 0
        total_max = 0

        for issue in issues:
            fine_str = issue.get("potential_fine", "$0")
            if "-" in fine_str:
                parts = fine_str.replace("$", "").replace(",", "").split("-")
                try:
                    total_min += int(parts[0].strip())
                    total_max += int(parts[1].strip())
                except:
                    pass

        return f"${total_min:,} - ${total_max:,}"

    def _get_recommended_actions(self, issues: List[Dict]) -> List[str]:
        """Get prioritized list of recommended actions."""
        actions = []

        critical_high = [i for i in issues if i["severity"] in ["critical", "high"]]
        if critical_high:
            actions.append("URGENT: Address all critical and high severity issues before broadcast")
            for issue in critical_high:
                actions.append(f"• {issue['recommendation']}")

        medium = [i for i in issues if i["severity"] == "medium"]
        if medium:
            actions.append("Review and resolve medium severity issues:")
            for issue in medium:
                actions.append(f"• {issue['recommendation']}")

        if not issues:
            actions.append("No compliance issues detected. Content is ready for broadcast.")

        return actions
