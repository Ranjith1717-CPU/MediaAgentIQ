"""
MediaAgentIQ - Notification & Alert Service

Multi-channel notification system for agent alerts:
- Email notifications
- Slack integration
- Webhook callbacks
- SMS (via Twilio)
- In-app notifications
- MAM system notifications
"""

import asyncio
import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import aiohttp

logger = logging.getLogger("notification_service")


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"           # General information
    SUCCESS = "success"     # Task completed successfully
    WARNING = "warning"     # Attention needed
    CRITICAL = "critical"   # Immediate action required
    URGENT = "urgent"       # Emergency - broadcast immediately


class AlertCategory(Enum):
    """Categories of alerts"""
    TRENDING = "trending"           # Trending topic detected
    COMPLIANCE = "compliance"       # Compliance violation
    RIGHTS = "rights"               # Rights/license issue
    VIRAL = "viral"                 # Viral content detected
    PROCESSING = "processing"       # Processing status
    SYSTEM = "system"               # System status
    ASSET = "asset"                 # New asset detected
    ERROR = "error"                 # Error occurred


@dataclass
class Alert:
    """Represents an alert/notification"""
    id: str
    title: str
    message: str
    level: AlertLevel
    category: AlertCategory
    timestamp: datetime = field(default_factory=datetime.now)
    source_agent: Optional[str] = None
    asset_id: Optional[str] = None
    asset_name: Optional[str] = None
    action_required: bool = False
    action_url: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    sent_channels: List[str] = field(default_factory=list)
    acknowledged: bool = False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "level": self.level.value,
            "category": self.category.value,
            "timestamp": self.timestamp.isoformat(),
            "source_agent": self.source_agent,
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "action_required": self.action_required,
            "action_url": self.action_url,
            "metadata": self.metadata,
            "acknowledged": self.acknowledged
        }

    def to_slack_block(self) -> Dict:
        """Format alert for Slack Block Kit"""
        emoji = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.SUCCESS: "✅",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🚨",
            AlertLevel.URGENT: "🔴"
        }

        color = {
            AlertLevel.INFO: "#3b82f6",
            AlertLevel.SUCCESS: "#22c55e",
            AlertLevel.WARNING: "#f59e0b",
            AlertLevel.CRITICAL: "#ef4444",
            AlertLevel.URGENT: "#dc2626"
        }

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji.get(self.level, '📢')} {self.title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": self.message
                }
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"*Agent:* {self.source_agent or 'System'}"},
                    {"type": "mrkdwn", "text": f"*Category:* {self.category.value}"},
                    {"type": "mrkdwn", "text": f"*Time:* {self.timestamp.strftime('%I:%M %p')}"}
                ]
            }
        ]

        if self.asset_name:
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"📁 *Asset:* {self.asset_name}"}
            })

        if self.action_required and self.action_url:
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Take Action"},
                        "url": self.action_url,
                        "style": "primary"
                    }
                ]
            })

        return {
            "attachments": [{
                "color": color.get(self.level, "#6b7280"),
                "blocks": blocks
            }]
        }


@dataclass
class NotificationConfig:
    """Configuration for notification channels"""
    # Email
    email_enabled: bool = False
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = ""
    email_to: List[str] = field(default_factory=list)

    # Slack
    slack_enabled: bool = False
    slack_webhook_url: str = ""
    slack_channel: str = "#mediaagentiq-alerts"

    # Webhooks
    webhook_enabled: bool = False
    webhook_urls: List[str] = field(default_factory=list)

    # In-app
    inapp_enabled: bool = True
    max_inapp_alerts: int = 100

    # Filtering
    min_level: AlertLevel = AlertLevel.INFO
    enabled_categories: List[str] = field(default_factory=lambda: ["all"])


class NotificationService:
    """
    Enterprise Notification Service

    Multi-channel alert system for MediaAgentIQ agents.
    Sends real-time notifications when agents detect important events.

    Channels:
    - Email (SMTP)
    - Slack (Webhooks)
    - Custom Webhooks (REST)
    - In-app notifications

    Features:
    - Alert prioritization and filtering
    - Rate limiting
    - Alert aggregation
    - Acknowledgment tracking
    """

    def __init__(self, config: Optional[NotificationConfig] = None):
        self.config = config or NotificationConfig()
        self.alerts: List[Alert] = []
        self.alert_count = 0
        self.listeners: List[Callable] = []

        # Rate limiting
        self.last_alerts: Dict[str, datetime] = {}  # category -> last alert time
        self.rate_limit_seconds = 60  # Minimum seconds between same-category alerts

        # Statistics
        self.stats = {
            "total_alerts": 0,
            "by_level": {level.value: 0 for level in AlertLevel},
            "by_category": {cat.value: 0 for cat in AlertCategory},
            "by_channel": {"email": 0, "slack": 0, "webhook": 0, "inapp": 0}
        }

        logger.info("NotificationService initialized")

    def add_listener(self, callback: Callable):
        """Add a listener for real-time alert notifications"""
        self.listeners.append(callback)

    def _generate_alert_id(self) -> str:
        """Generate unique alert ID"""
        self.alert_count += 1
        return f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.alert_count:04d}"

    def _should_send(self, alert: Alert) -> bool:
        """Check if alert should be sent based on config and rate limiting"""
        # Check level
        level_order = list(AlertLevel)
        if level_order.index(alert.level) < level_order.index(self.config.min_level):
            return False

        # Check category
        if "all" not in self.config.enabled_categories:
            if alert.category.value not in self.config.enabled_categories:
                return False

        # Rate limiting (skip for critical/urgent)
        if alert.level not in [AlertLevel.CRITICAL, AlertLevel.URGENT]:
            last_time = self.last_alerts.get(alert.category.value)
            if last_time:
                elapsed = (datetime.now() - last_time).total_seconds()
                if elapsed < self.rate_limit_seconds:
                    logger.debug(f"Rate limited: {alert.category.value}")
                    return False

        return True

    async def send_alert(self, alert: Alert) -> bool:
        """Send an alert through configured channels"""
        if not self._should_send(alert):
            return False

        alert.id = self._generate_alert_id()
        success = False

        # Update rate limiting
        self.last_alerts[alert.category.value] = datetime.now()

        # Send to all configured channels
        tasks = []

        if self.config.email_enabled:
            tasks.append(self._send_email(alert))

        if self.config.slack_enabled:
            tasks.append(self._send_slack(alert))

        if self.config.webhook_enabled:
            tasks.append(self._send_webhooks(alert))

        if self.config.inapp_enabled:
            self._add_inapp(alert)
            success = True

        # Execute all channel sends
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            success = any(r is True for r in results if not isinstance(r, Exception))

        # Update stats
        self.stats["total_alerts"] += 1
        self.stats["by_level"][alert.level.value] += 1
        self.stats["by_category"][alert.category.value] += 1

        # Notify listeners
        for listener in self.listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(alert)
                else:
                    listener(alert)
            except Exception as e:
                logger.error(f"Listener error: {e}")

        logger.info(f"Alert sent: [{alert.level.value}] {alert.title}")
        return success

    async def _send_email(self, alert: Alert) -> bool:
        """Send alert via email"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"[MediaAgentIQ {alert.level.value.upper()}] {alert.title}"
            msg["From"] = self.config.email_from
            msg["To"] = ", ".join(self.config.email_to)

            # HTML email body
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background: #1e293b; color: #e2e8f0; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: #0f172a; border-radius: 12px; padding: 24px;">
                    <h1 style="color: {'#ef4444' if alert.level in [AlertLevel.CRITICAL, AlertLevel.URGENT] else '#f59e0b' if alert.level == AlertLevel.WARNING else '#22c55e'};">
                        {alert.title}
                    </h1>
                    <p style="font-size: 16px; line-height: 1.6;">{alert.message}</p>

                    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #334155;"><strong>Agent:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #334155;">{alert.source_agent or 'System'}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #334155;"><strong>Category:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #334155;">{alert.category.value}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #334155;"><strong>Time:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #334155;">{alert.timestamp.strftime('%Y-%m-%d %I:%M %p')}</td>
                        </tr>
                        {f'<tr><td style="padding: 8px;"><strong>Asset:</strong></td><td style="padding: 8px;">{alert.asset_name}</td></tr>' if alert.asset_name else ''}
                    </table>

                    {f'<a href="{alert.action_url}" style="display: inline-block; margin-top: 20px; padding: 12px 24px; background: #6366f1; color: white; text-decoration: none; border-radius: 8px;">Take Action</a>' if alert.action_url else ''}

                    <p style="margin-top: 30px; font-size: 12px; color: #64748b;">
                        This alert was generated by MediaAgentIQ Autonomous Agent Platform
                    </p>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(html, "html"))

            # Send email
            with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_user, self.config.smtp_password)
                server.sendmail(self.config.email_from, self.config.email_to, msg.as_string())

            alert.sent_channels.append("email")
            self.stats["by_channel"]["email"] += 1
            return True

        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False

    async def _send_slack(self, alert: Alert) -> bool:
        """Send alert to Slack"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = alert.to_slack_block()
                async with session.post(
                    self.config.slack_webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        alert.sent_channels.append("slack")
                        self.stats["by_channel"]["slack"] += 1
                        return True
                    else:
                        logger.error(f"Slack send failed: {response.status}")
                        return False

        except Exception as e:
            logger.error(f"Slack send failed: {e}")
            return False

    async def _send_webhooks(self, alert: Alert) -> bool:
        """Send alert to configured webhooks"""
        success = False
        try:
            async with aiohttp.ClientSession() as session:
                for url in self.config.webhook_urls:
                    try:
                        async with session.post(
                            url,
                            json=alert.to_dict(),
                            headers={"Content-Type": "application/json"}
                        ) as response:
                            if response.status in [200, 201, 202]:
                                success = True
                    except Exception as e:
                        logger.error(f"Webhook failed ({url}): {e}")

            if success:
                alert.sent_channels.append("webhook")
                self.stats["by_channel"]["webhook"] += 1

        except Exception as e:
            logger.error(f"Webhooks send failed: {e}")

        return success

    def _add_inapp(self, alert: Alert):
        """Add alert to in-app notification list"""
        self.alerts.insert(0, alert)
        alert.sent_channels.append("inapp")
        self.stats["by_channel"]["inapp"] += 1

        # Trim old alerts
        if len(self.alerts) > self.config.max_inapp_alerts:
            self.alerts = self.alerts[:self.config.max_inapp_alerts]

    def get_alerts(self, limit: int = 50, level: Optional[AlertLevel] = None,
                   category: Optional[AlertCategory] = None,
                   unacknowledged_only: bool = False) -> List[Alert]:
        """Get alerts with optional filtering"""
        alerts = self.alerts

        if level:
            alerts = [a for a in alerts if a.level == level]

        if category:
            alerts = [a for a in alerts if a.category == category]

        if unacknowledged_only:
            alerts = [a for a in alerts if not a.acknowledged]

        return alerts[:limit]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark an alert as acknowledged"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False

    def get_stats(self) -> Dict:
        """Get notification statistics"""
        return {
            **self.stats,
            "pending_alerts": len([a for a in self.alerts if not a.acknowledged]),
            "config": {
                "email_enabled": self.config.email_enabled,
                "slack_enabled": self.config.slack_enabled,
                "webhook_enabled": self.config.webhook_enabled,
                "inapp_enabled": self.config.inapp_enabled
            }
        }


# Helper functions for creating common alerts
def create_trending_alert(topic: str, velocity: int, source_agent: str = "Trending Agent") -> Alert:
    """Create a trending topic alert"""
    level = AlertLevel.URGENT if velocity > 90 else AlertLevel.WARNING if velocity > 70 else AlertLevel.INFO
    return Alert(
        id="",
        title=f"Trending Topic Detected: {topic}",
        message=f"Topic '{topic}' is trending with velocity score {velocity}/100. Consider creating content or coverage.",
        level=level,
        category=AlertCategory.TRENDING,
        source_agent=source_agent,
        action_required=velocity > 80,
        metadata={"topic": topic, "velocity": velocity}
    )


def create_compliance_alert(issue_type: str, severity: str, timestamp: str,
                           asset_name: str, source_agent: str = "Compliance Agent") -> Alert:
    """Create a compliance violation alert"""
    level = AlertLevel.CRITICAL if severity == "critical" else AlertLevel.WARNING
    return Alert(
        id="",
        title=f"Compliance Issue: {issue_type.upper()}",
        message=f"Compliance violation detected at {timestamp}. Severity: {severity}. Immediate review recommended.",
        level=level,
        category=AlertCategory.COMPLIANCE,
        source_agent=source_agent,
        asset_name=asset_name,
        action_required=True,
        metadata={"issue_type": issue_type, "severity": severity, "timestamp": timestamp}
    )


def create_rights_alert(license_name: str, days_remaining: int, cost: str,
                       source_agent: str = "Rights Agent") -> Alert:
    """Create a rights/license expiration alert"""
    level = AlertLevel.CRITICAL if days_remaining <= 7 else AlertLevel.WARNING if days_remaining <= 30 else AlertLevel.INFO
    return Alert(
        id="",
        title=f"License Expiring: {license_name}",
        message=f"License '{license_name}' expires in {days_remaining} days. Cost to renew: {cost}",
        level=level,
        category=AlertCategory.RIGHTS,
        source_agent=source_agent,
        action_required=days_remaining <= 14,
        metadata={"license": license_name, "days_remaining": days_remaining, "cost": cost}
    )


def create_viral_alert(clip_title: str, score: float, platforms: List[str],
                      predicted_views: str, source_agent: str = "Clip Agent") -> Alert:
    """Create a viral content detection alert"""
    level = AlertLevel.SUCCESS if score > 0.9 else AlertLevel.INFO
    return Alert(
        id="",
        title=f"Viral Content Detected: {clip_title}",
        message=f"Viral moment found with {score*100:.0f}% viral score. Predicted reach: {predicted_views}. Best platforms: {', '.join(platforms)}",
        level=level,
        category=AlertCategory.VIRAL,
        source_agent=source_agent,
        action_required=score > 0.9,
        metadata={"score": score, "platforms": platforms, "predicted_views": predicted_views}
    )


def create_asset_alert(filename: str, asset_type: str, size_mb: float,
                      watch_folder: str, source_agent: str = "Folder Watcher") -> Alert:
    """Create a new asset detection alert"""
    return Alert(
        id="",
        title=f"New Asset Detected: {filename}",
        message=f"New {asset_type} file ({size_mb:.2f} MB) detected in '{watch_folder}'. Processing started.",
        level=AlertLevel.INFO,
        category=AlertCategory.ASSET,
        source_agent=source_agent,
        asset_name=filename,
        metadata={"asset_type": asset_type, "size_mb": size_mb, "watch_folder": watch_folder}
    )
