"""
Compliance Agent - Monitors 24/7 for FCC violations, profanity, political ad issues
"""
import random
from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime
from .base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    """Agent for monitoring FCC compliance and content violations."""

    def __init__(self):
        super().__init__(
            name="Compliance Agent",
            description="Monitors 24/7 for FCC violations, profanity, political ad issues, auto-logs and alerts"
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

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Scan content for compliance issues."""
        if not await self.validate_input(input_data):
            return self.create_response(False, error="Invalid input for compliance scan")

        # Run all compliance checks
        issues = []
        issues.extend(await self._check_profanity(input_data))
        issues.extend(await self._check_political_ads(input_data))
        issues.extend(await self._check_sponsor_identification(input_data))
        issues.extend(await self._check_caption_compliance(input_data))
        issues.extend(await self._check_eas_compliance(input_data))

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

    async def _check_profanity(self, input_data: Any) -> List[Dict]:
        """Check for profanity/indecent content."""
        issues = []

        # Demo: Generate mock profanity detection
        mock_detections = [
            {
                "word": "damn",
                "timestamp": 125.5,
                "context": "...what the damn problem is with...",
                "confidence": 0.95
            }
        ]

        for detection in mock_detections:
            issues.append({
                "id": f"prof_{random.randint(1000, 9999)}",
                "type": "profanity",
                "severity": "high",
                "timestamp": detection["timestamp"],
                "timestamp_formatted": self.format_timestamp(detection["timestamp"]),
                "description": f"Potential profanity detected: '{detection['word']}'",
                "context": detection["context"],
                "confidence": detection["confidence"],
                "fcc_rule": "47 U.S.C. § 326",
                "potential_fine": "$25,000 - $500,000",
                "recommendation": "Review segment, consider bleeping or re-recording",
                "action_required": True
            })

        return issues

    async def _check_political_ads(self, input_data: Any) -> List[Dict]:
        """Check for political advertising compliance."""
        issues = []

        # Demo: Mock political ad detection
        mock_political_content = {
            "timestamp": 450.0,
            "text": "Vote for candidate Johnson this November",
            "missing_disclosure": True
        }

        if mock_political_content["missing_disclosure"]:
            issues.append({
                "id": f"pol_{random.randint(1000, 9999)}",
                "type": "political_ad",
                "severity": "medium",
                "timestamp": mock_political_content["timestamp"],
                "timestamp_formatted": self.format_timestamp(mock_political_content["timestamp"]),
                "description": "Political content detected without proper disclosure",
                "context": mock_political_content["text"],
                "confidence": 0.88,
                "fcc_rule": "47 U.S.C. § 315",
                "potential_fine": "$10,000 - $100,000",
                "recommendation": "Add 'Paid for by...' disclosure statement",
                "action_required": True,
                "disclosure_template": "Paid for by [Committee Name]. Authorized by [Candidate Name] for [Office]."
            })

        return issues

    async def _check_sponsor_identification(self, input_data: Any) -> List[Dict]:
        """Check for sponsor identification compliance."""
        issues = []

        # Demo: Mock sponsored content without ID
        issues.append({
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
        })

        return issues

    async def _check_caption_compliance(self, input_data: Any) -> List[Dict]:
        """Check closed captioning compliance."""
        issues = []

        # Demo: Caption quality issues
        issues.append({
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
        })

        return issues

    async def _check_eas_compliance(self, input_data: Any) -> List[Dict]:
        """Check Emergency Alert System compliance."""
        # In production, would check for proper EAS handling
        return []  # No issues in demo

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

        # Simplified calculation
        total_min = 0
        total_max = 0

        for issue in issues:
            fine_str = issue.get("potential_fine", "$0")
            # Parse fine range (simplified)
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

        # Group actions by priority
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
