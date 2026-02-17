"""
Rights Agent - Tracks content licenses, alerts before expiry, monitors unauthorized usage
"""
import random
from typing import Any, Dict, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent


class RightsAgent(BaseAgent):
    """Agent for managing content rights and licenses."""

    def __init__(self):
        super().__init__(
            name="Rights Agent",
            description="Tracks content licenses, alerts before expiry, monitors unauthorized usage"
        )

        self.license_types = {
            "exclusive": {"priority": "high", "renewal_notice_days": 90},
            "non_exclusive": {"priority": "medium", "renewal_notice_days": 60},
            "limited": {"priority": "medium", "renewal_notice_days": 30},
            "perpetual": {"priority": "low", "renewal_notice_days": 0},
            "time_limited": {"priority": "high", "renewal_notice_days": 45}
        }

        self.usage_rights = [
            "broadcast", "streaming", "social_media", "archive",
            "syndication", "international", "clip_licensing"
        ]

    async def validate_input(self, input_data: Any) -> bool:
        """Validate input for rights management."""
        if not input_data:
            return False
        return True

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process rights management request."""
        if not await self.validate_input(input_data):
            return self.create_response(False, error="Invalid input for rights management")

        # Get current licenses
        licenses = await self._get_licenses()

        # Check for expiring licenses
        expiring = await self._check_expiring_licenses(licenses)

        # Monitor for unauthorized usage
        violations = await self._check_unauthorized_usage()

        # Generate alerts
        alerts = await self._generate_alerts(expiring, violations)

        # Create rights report
        report = await self._generate_report(licenses, expiring, violations)

        return self.create_response(True, data={
            "licenses": licenses,
            "expiring_soon": expiring,
            "violations": violations,
            "alerts": alerts,
            "report": report,
            "stats": {
                "total_licenses": len(licenses),
                "active_licenses": len([l for l in licenses if l["status"] == "active"]),
                "expiring_30_days": len([l for l in expiring if l["days_until_expiry"] <= 30]),
                "violations_detected": len(violations),
                "total_content_value": "$2.5M"
            }
        })

    async def _get_licenses(self) -> List[Dict]:
        """Get all content licenses."""
        licenses = [
            {
                "id": "LIC001",
                "content_title": "Premier League Highlights Package",
                "content_type": "sports",
                "licensor": "Premier League Media",
                "license_type": "time_limited",
                "rights": ["broadcast", "streaming", "social_media"],
                "territories": ["United States", "Canada"],
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "status": "active",
                "cost": "$500,000/year",
                "auto_renewal": False,
                "contact": "licensing@premierleague.com"
            },
            {
                "id": "LIC002",
                "content_title": "AP News Feed",
                "content_type": "news",
                "licensor": "Associated Press",
                "license_type": "exclusive",
                "rights": ["broadcast", "streaming", "archive"],
                "territories": ["United States"],
                "start_date": "2024-06-01",
                "end_date": "2025-05-31",
                "status": "active",
                "cost": "$750,000/year",
                "auto_renewal": True,
                "contact": "media@ap.org"
            },
            {
                "id": "LIC003",
                "content_title": "Stock Footage Library - Nature",
                "content_type": "stock",
                "licensor": "Getty Images",
                "license_type": "non_exclusive",
                "rights": ["broadcast", "streaming", "social_media", "archive"],
                "territories": ["Worldwide"],
                "start_date": "2024-03-15",
                "end_date": "2025-03-14",
                "status": "active",
                "cost": "$50,000/year",
                "auto_renewal": True,
                "contact": "corporate@gettyimages.com"
            },
            {
                "id": "LIC004",
                "content_title": "Music Licensing - Production Library",
                "content_type": "music",
                "licensor": "Epidemic Sound",
                "license_type": "perpetual",
                "rights": ["broadcast", "streaming", "social_media", "syndication"],
                "territories": ["Worldwide"],
                "start_date": "2023-01-01",
                "end_date": None,
                "status": "active",
                "cost": "$25,000 (one-time)",
                "auto_renewal": False,
                "contact": "enterprise@epidemicsound.com"
            },
            {
                "id": "LIC005",
                "content_title": "Reuters Video Package",
                "content_type": "news",
                "licensor": "Reuters",
                "license_type": "time_limited",
                "rights": ["broadcast", "streaming"],
                "territories": ["North America"],
                "start_date": "2024-04-01",
                "end_date": "2025-01-15",
                "status": "active",
                "cost": "$300,000/year",
                "auto_renewal": False,
                "contact": "mediaservices@reuters.com"
            }
        ]

        return licenses

    async def _check_expiring_licenses(self, licenses: List[Dict]) -> List[Dict]:
        """Check for licenses expiring soon."""
        expiring = []
        today = datetime.now().date()

        for license in licenses:
            if license.get("end_date"):
                end_date = datetime.strptime(license["end_date"], "%Y-%m-%d").date()
                days_until = (end_date - today).days

                if days_until <= 90:
                    expiring.append({
                        **license,
                        "days_until_expiry": days_until,
                        "urgency": "critical" if days_until <= 14 else "high" if days_until <= 30 else "medium",
                        "recommended_action": "Initiate renewal negotiations" if not license.get("auto_renewal") else "Confirm auto-renewal terms"
                    })

        expiring.sort(key=lambda x: x["days_until_expiry"])
        return expiring

    async def _check_unauthorized_usage(self) -> List[Dict]:
        """Monitor for unauthorized content usage."""
        # Mock unauthorized usage detections
        violations = [
            {
                "id": f"VIO{random.randint(1000, 9999)}",
                "type": "unauthorized_rebroadcast",
                "severity": "high",
                "content_title": "Premier League Highlights Package",
                "detected_on": "YouTube",
                "detected_url": "https://youtube.com/watch?v=xxxxx",
                "detected_at": datetime.now().isoformat(),
                "uploader": "SportsHighlightsUnofficial",
                "view_count": 150000,
                "status": "active",
                "recommended_action": "File DMCA takedown request",
                "estimated_damages": "$25,000"
            },
            {
                "id": f"VIO{random.randint(1000, 9999)}",
                "type": "territorial_violation",
                "severity": "medium",
                "content_title": "AP News Feed",
                "detected_on": "International Streaming Platform",
                "detected_url": "https://example-stream.com/news",
                "detected_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "uploader": "NewsAggregator",
                "view_count": 50000,
                "status": "investigating",
                "recommended_action": "Contact platform for removal",
                "estimated_damages": "$10,000"
            }
        ]

        return violations

    async def _generate_alerts(self, expiring: List[Dict], violations: List[Dict]) -> List[Dict]:
        """Generate alerts for rights issues."""
        alerts = []

        # Expiring license alerts
        for license in expiring:
            urgency = license.get("urgency", "medium")
            alerts.append({
                "id": f"ALERT{random.randint(1000, 9999)}",
                "type": "license_expiry",
                "urgency": urgency,
                "title": f"License Expiring: {license['content_title']}",
                "message": f"License expires in {license['days_until_expiry']} days. {license['recommended_action']}.",
                "created_at": datetime.now().isoformat(),
                "action_url": f"/rights/license/{license['id']}",
                "dismissed": False
            })

        # Violation alerts
        for violation in violations:
            alerts.append({
                "id": f"ALERT{random.randint(1000, 9999)}",
                "type": "unauthorized_usage",
                "urgency": violation["severity"],
                "title": f"Unauthorized Usage: {violation['content_title']}",
                "message": f"Detected on {violation['detected_on']}. {violation['recommended_action']}.",
                "created_at": violation["detected_at"],
                "action_url": f"/rights/violation/{violation['id']}",
                "dismissed": False
            })

        # Sort by urgency
        urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        alerts.sort(key=lambda x: urgency_order.get(x["urgency"], 4))

        return alerts

    async def _generate_report(self, licenses: List[Dict], expiring: List[Dict], violations: List[Dict]) -> Dict:
        """Generate comprehensive rights report."""
        return {
            "report_id": f"RPT{random.randint(10000, 99999)}",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_licenses": len(licenses),
                "active_licenses": len([l for l in licenses if l["status"] == "active"]),
                "expiring_soon": len(expiring),
                "active_violations": len([v for v in violations if v["status"] == "active"]),
                "total_annual_cost": "$1,625,000",
                "potential_damages": sum(int(v["estimated_damages"].replace("$", "").replace(",", "")) for v in violations)
            },
            "license_breakdown": {
                "by_type": {
                    "exclusive": len([l for l in licenses if l["license_type"] == "exclusive"]),
                    "non_exclusive": len([l for l in licenses if l["license_type"] == "non_exclusive"]),
                    "time_limited": len([l for l in licenses if l["license_type"] == "time_limited"]),
                    "perpetual": len([l for l in licenses if l["license_type"] == "perpetual"])
                },
                "by_content_type": {
                    "news": len([l for l in licenses if l["content_type"] == "news"]),
                    "sports": len([l for l in licenses if l["content_type"] == "sports"]),
                    "stock": len([l for l in licenses if l["content_type"] == "stock"]),
                    "music": len([l for l in licenses if l["content_type"] == "music"])
                }
            },
            "action_items": [
                {"priority": "high", "action": "Renew Premier League Highlights Package", "deadline": "2024-10-01"},
                {"priority": "high", "action": "File DMCA for YouTube violation", "deadline": "Immediate"},
                {"priority": "medium", "action": "Review Reuters renewal terms", "deadline": "2024-11-15"},
                {"priority": "low", "action": "Audit music usage compliance", "deadline": "2024-12-31"}
            ],
            "recommendations": [
                "Implement automated content fingerprinting for violation detection",
                "Negotiate multi-year deals for stable pricing",
                "Consider territorial expansion for top-performing content",
                "Set up automated renewal alerts 90 days before expiry"
            ]
        }
