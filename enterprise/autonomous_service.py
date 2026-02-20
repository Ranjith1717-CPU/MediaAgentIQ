"""
MediaAgentIQ - Autonomous Background Service

Main service that orchestrates:
- Folder watching for new assets
- Automatic agent processing
- MAM system integration
- Alert notifications
- Background scheduling

This service runs continuously and processes content
without manual intervention.
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

from .folder_watcher import FolderWatcher, WatchConfig, DetectedAsset
from .notification_service import (
    NotificationService, NotificationConfig, Alert, AlertLevel, AlertCategory,
    create_trending_alert, create_compliance_alert, create_rights_alert,
    create_viral_alert, create_asset_alert
)
from .mam_connector import MAMConnector, MAMConfig, create_connector

logger = logging.getLogger("autonomous_service")


class ServiceStatus(Enum):
    """Service status"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class ProcessingResult:
    """Result of processing an asset through agents"""
    asset_path: str
    asset_name: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    agents_run: List[str] = field(default_factory=list)
    results: Dict = field(default_factory=dict)
    alerts_generated: List[str] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "asset_path": self.asset_path,
            "asset_name": self.asset_name,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "agents_run": self.agents_run,
            "results": self.results,
            "alerts_generated": self.alerts_generated,
            "success": self.success,
            "error": self.error
        }


@dataclass
class ServiceConfig:
    """Configuration for the autonomous service"""
    # Processing
    max_concurrent_jobs: int = 3
    processing_timeout_seconds: int = 300

    # Watch folders
    watch_folders: List[WatchConfig] = field(default_factory=list)

    # MAM connections
    mam_configs: List[MAMConfig] = field(default_factory=list)

    # Notifications
    notification_config: NotificationConfig = field(default_factory=NotificationConfig)

    # Scheduling
    trending_check_interval: int = 300  # 5 minutes
    compliance_check_interval: int = 600  # 10 minutes
    rights_check_interval: int = 3600  # 1 hour

    # Demo mode
    demo_mode: bool = True  # Use mock processing in demo mode


class AutonomousService:
    """
    MediaAgentIQ Autonomous Background Service

    Runs continuously in the background, monitoring for new content
    and automatically processing it through the AI agent pipeline.

    Features:
    - Multi-folder watching (MAM hot folders, ingest directories)
    - Automatic agent triggering based on content type
    - MAM system integration (Avid, Grass Valley, etc.)
    - Real-time notifications and alerts
    - Scheduled background tasks
    - Event-driven processing chains

    Usage:
        service = AutonomousService(config)
        await service.start()
    """

    def __init__(self, config: Optional[ServiceConfig] = None):
        self.config = config or ServiceConfig()
        self.status = ServiceStatus.STOPPED

        # Initialize components
        self.folder_watcher = FolderWatcher()
        self.notification_service = NotificationService(self.config.notification_config)
        self.mam_connectors: Dict[str, MAMConnector] = {}

        # Processing state
        self.processing_queue: asyncio.Queue = asyncio.Queue()
        self.active_jobs: Dict[str, ProcessingResult] = {}
        self.completed_jobs: List[ProcessingResult] = []

        # Background tasks
        self._tasks: List[asyncio.Task] = []

        # Statistics
        self.stats = {
            "start_time": None,
            "total_processed": 0,
            "total_alerts": 0,
            "by_agent": {},
            "last_activity": None
        }

        # State persistence
        self.state_file = Path("enterprise/service_state.json")

        logger.info("AutonomousService initialized")

    async def start(self):
        """Start the autonomous service"""
        if self.status == ServiceStatus.RUNNING:
            logger.warning("Service already running")
            return

        self.status = ServiceStatus.STARTING
        logger.info("Starting AutonomousService...")

        try:
            # Initialize watch folders
            await self._setup_watch_folders()

            # Connect to MAM systems
            await self._connect_mam_systems()

            # Set up folder watcher callbacks
            self.folder_watcher.on_asset_ready = self._on_asset_detected

            # Start background tasks
            self._tasks = [
                asyncio.create_task(self.folder_watcher.start()),
                asyncio.create_task(self._process_queue()),
                asyncio.create_task(self._scheduled_trending_check()),
                asyncio.create_task(self._scheduled_compliance_check()),
                asyncio.create_task(self._scheduled_rights_check()),
            ]

            self.status = ServiceStatus.RUNNING
            self.stats["start_time"] = datetime.now().isoformat()

            logger.info("AutonomousService started successfully")

            # Send startup notification
            await self.notification_service.send_alert(Alert(
                id="",
                title="MediaAgentIQ Service Started",
                message=f"Autonomous processing service is now running. Monitoring {len(self.config.watch_folders)} folders.",
                level=AlertLevel.SUCCESS,
                category=AlertCategory.SYSTEM,
                source_agent="Autonomous Service"
            ))

        except Exception as e:
            self.status = ServiceStatus.ERROR
            logger.error(f"Failed to start service: {e}")
            raise

    async def stop(self):
        """Stop the autonomous service"""
        if self.status != ServiceStatus.RUNNING:
            return

        self.status = ServiceStatus.STOPPING
        logger.info("Stopping AutonomousService...")

        # Stop folder watcher
        self.folder_watcher.stop()

        # Cancel background tasks
        for task in self._tasks:
            task.cancel()

        # Disconnect MAM systems
        for connector in self.mam_connectors.values():
            await connector.disconnect()

        # Save state
        self._save_state()

        self.status = ServiceStatus.STOPPED
        logger.info("AutonomousService stopped")

    async def _setup_watch_folders(self):
        """Set up configured watch folders"""
        for watch_config in self.config.watch_folders:
            self.folder_watcher.add_watch_folder(watch_config)

        # Add default demo folder if no folders configured
        if not self.config.watch_folders:
            demo_folder = WatchConfig(
                path="demo_assets",
                name="Demo Assets",
                file_types=["video", "audio"],
                trigger_agents=["all"]
            )
            self.folder_watcher.add_watch_folder(demo_folder)

    async def _connect_mam_systems(self):
        """Connect to configured MAM systems"""
        for mam_config in self.config.mam_configs:
            connector = create_connector(mam_config)
            success = await connector.connect()

            if success:
                self.mam_connectors[mam_config.name] = connector
                logger.info(f"Connected to MAM: {mam_config.name}")
            else:
                logger.warning(f"Failed to connect to MAM: {mam_config.name}")

    async def _on_asset_detected(self, asset: DetectedAsset):
        """Handle detected asset - queue for processing"""
        logger.info(f"Asset detected: {asset.filename}")

        # Create processing job
        result = ProcessingResult(
            asset_path=asset.path,
            asset_name=asset.filename,
            started_at=datetime.now()
        )

        # Send asset detection alert
        await self.notification_service.send_alert(
            create_asset_alert(
                filename=asset.filename,
                asset_type=asset.asset_type.value,
                size_mb=asset.size_mb,
                watch_folder=asset.watch_config.name
            )
        )

        # Queue for processing
        await self.processing_queue.put((asset, result))
        self.stats["last_activity"] = datetime.now().isoformat()

    async def _process_queue(self):
        """Process queued assets through agents"""
        while self.status in [ServiceStatus.STARTING, ServiceStatus.RUNNING]:
            try:
                # Get next asset to process
                asset, result = await asyncio.wait_for(
                    self.processing_queue.get(),
                    timeout=1.0
                )

                # Add to active jobs
                self.active_jobs[asset.path] = result

                # Process through agents
                await self._process_asset(asset, result)

                # Move to completed
                del self.active_jobs[asset.path]
                self.completed_jobs.append(result)
                self.stats["total_processed"] += 1

                # Keep only last 100 completed jobs
                if len(self.completed_jobs) > 100:
                    self.completed_jobs = self.completed_jobs[-100:]

            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Processing error: {e}")

    async def _process_asset(self, asset: DetectedAsset, result: ProcessingResult):
        """Process an asset through the agent pipeline"""
        agents_to_run = asset.watch_config.trigger_agents

        if "all" in agents_to_run:
            agents_to_run = ["caption", "clip", "compliance", "archive", "social", "localization", "rights", "trending"]

        logger.info(f"Processing {asset.filename} through agents: {agents_to_run}")

        for agent_name in agents_to_run:
            try:
                agent_result = await self._run_agent(agent_name, asset)
                result.agents_run.append(agent_name)
                result.results[agent_name] = agent_result

                # Update stats
                self.stats["by_agent"][agent_name] = self.stats["by_agent"].get(agent_name, 0) + 1

                # Generate alerts based on results
                alerts = await self._generate_alerts_from_result(agent_name, agent_result, asset)
                result.alerts_generated.extend([a.title for a in alerts])

            except Exception as e:
                logger.error(f"Agent {agent_name} failed: {e}")
                result.results[agent_name] = {"error": str(e)}

        result.completed_at = datetime.now()

        # Notify MAM systems
        await self._notify_mam_systems(asset, result)

        logger.info(f"Completed processing {asset.filename}")

    async def _run_agent(self, agent_name: str, asset: DetectedAsset) -> Dict:
        """Run a specific agent on an asset"""
        if self.config.demo_mode:
            # Return mock results in demo mode
            return await self._get_demo_agent_result(agent_name, asset)

        # Import and run actual agent
        try:
            if agent_name == "caption":
                from agents import CaptionAgent
                agent = CaptionAgent()
                return await agent.process(asset.path)

            elif agent_name == "clip":
                from agents import ClipAgent
                agent = ClipAgent()
                return await agent.process(asset.path)

            elif agent_name == "compliance":
                from agents import ComplianceAgent
                agent = ComplianceAgent()
                return await agent.process(asset.path)

            elif agent_name == "archive":
                from agents import ArchiveAgent
                agent = ArchiveAgent()
                return await agent.process(asset.path)

            elif agent_name == "social":
                from agents import SocialPublishingAgent
                agent = SocialPublishingAgent()
                return await agent.process(asset.path)

            elif agent_name == "localization":
                from agents import LocalizationAgent
                agent = LocalizationAgent()
                return await agent.process(asset.path)

            elif agent_name == "rights":
                from agents import RightsAgent
                agent = RightsAgent()
                return await agent.process(asset.path)

            elif agent_name == "trending":
                from agents import TrendingAgent
                agent = TrendingAgent()
                return await agent.process(asset.path)

        except Exception as e:
            logger.error(f"Agent execution error: {e}")
            return {"error": str(e)}

        return {"status": "unknown_agent"}

    async def _get_demo_agent_result(self, agent_name: str, asset: DetectedAsset) -> Dict:
        """Get demo results for an agent"""
        # Simulate processing time
        await asyncio.sleep(0.5)

        demo_results = {
            "caption": {
                "success": True,
                "segments": 8,
                "speakers": 1,
                "confidence": 0.97,
                "duration": "0:15"
            },
            "clip": {
                "success": True,
                "viral_moments": 2,
                "top_score": 0.94,
                "platforms": ["TikTok", "Instagram", "YouTube Shorts"]
            },
            "compliance": {
                "success": True,
                "issues": 0,
                "status": "cleared",
                "rating": "G"
            },
            "archive": {
                "success": True,
                "tags_generated": 8,
                "categories": ["entertainment", "music"],
                "indexed": True
            },
            "social": {
                "success": True,
                "posts_generated": 5,
                "platforms": ["TikTok", "Instagram", "Twitter/X", "Facebook", "YouTube"],
                "scheduled": True
            },
            "localization": {
                "success": True,
                "languages": 8,
                "quality_avg": 95,
                "voice_dub_available": True
            },
            "rights": {
                "success": True,
                "licenses_valid": True,
                "expiring_soon": 0,
                "violations": 0
            },
            "trending": {
                "success": True,
                "matching_trends": 3,
                "top_trend": "#Entertainment",
                "velocity": 82
            }
        }

        return demo_results.get(agent_name, {"success": True})

    async def _generate_alerts_from_result(self, agent_name: str, result: Dict, asset: DetectedAsset) -> List[Alert]:
        """Generate alerts based on agent results"""
        alerts = []

        if agent_name == "clip" and result.get("viral_moments", 0) > 0:
            alert = create_viral_alert(
                clip_title=f"Viral moment in {asset.filename}",
                score=result.get("top_score", 0.9),
                platforms=result.get("platforms", []),
                predicted_views="100K - 500K",
                source_agent="Clip Agent"
            )
            await self.notification_service.send_alert(alert)
            alerts.append(alert)

        if agent_name == "compliance" and result.get("issues", 0) > 0:
            alert = create_compliance_alert(
                issue_type="content_review",
                severity="warning",
                timestamp="00:00",
                asset_name=asset.filename,
                source_agent="Compliance Agent"
            )
            await self.notification_service.send_alert(alert)
            alerts.append(alert)

        if agent_name == "trending" and result.get("velocity", 0) > 80:
            alert = create_trending_alert(
                topic=result.get("top_trend", "#Trending"),
                velocity=result.get("velocity", 80),
                source_agent="Trending Agent"
            )
            await self.notification_service.send_alert(alert)
            alerts.append(alert)

        if agent_name == "rights" and result.get("expiring_soon", 0) > 0:
            alert = create_rights_alert(
                license_name="Content License",
                days_remaining=result.get("expiring_soon", 30),
                cost="Contact licensor",
                source_agent="Rights Agent"
            )
            await self.notification_service.send_alert(alert)
            alerts.append(alert)

        return alerts

    async def _notify_mam_systems(self, asset: DetectedAsset, result: ProcessingResult):
        """Notify connected MAM systems about processing completion"""
        for name, connector in self.mam_connectors.items():
            try:
                # Send processing complete event
                await connector.notify_event("asset_processed", {
                    "asset_path": asset.path,
                    "asset_name": asset.filename,
                    "agents_run": result.agents_run,
                    "success": result.success,
                    "timestamp": datetime.now().isoformat()
                })

                # Update metadata in MAM
                metadata = {
                    "mediaagentiq_processed": True,
                    "mediaagentiq_timestamp": datetime.now().isoformat(),
                    "mediaagentiq_agents": ",".join(result.agents_run)
                }

                # Add agent-specific metadata
                if "caption" in result.results:
                    metadata["has_captions"] = True
                    metadata["caption_segments"] = result.results["caption"].get("segments", 0)

                if "clip" in result.results:
                    metadata["viral_score"] = result.results["clip"].get("top_score", 0)

                if "archive" in result.results:
                    tags = result.results["archive"].get("categories", [])
                    if tags:
                        await connector.add_tags(asset.path, tags)

                logger.info(f"Notified MAM: {name}")

            except Exception as e:
                logger.error(f"MAM notification failed ({name}): {e}")

    async def _scheduled_trending_check(self):
        """Periodic trending topic check"""
        while self.status in [ServiceStatus.STARTING, ServiceStatus.RUNNING]:
            try:
                await asyncio.sleep(self.config.trending_check_interval)

                if self.config.demo_mode:
                    # Demo: Occasionally generate trending alerts
                    import random
                    if random.random() > 0.7:
                        await self.notification_service.send_alert(
                            create_trending_alert(
                                topic=random.choice(["#Entertainment", "#Viral", "#Breaking", "#Trending"]),
                                velocity=random.randint(70, 95),
                                source_agent="Trending Agent"
                            )
                        )

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Trending check error: {e}")

    async def _scheduled_compliance_check(self):
        """Periodic compliance monitoring"""
        while self.status in [ServiceStatus.STARTING, ServiceStatus.RUNNING]:
            try:
                await asyncio.sleep(self.config.compliance_check_interval)
                # In production, this would run actual compliance checks
                logger.debug("Compliance check completed")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Compliance check error: {e}")

    async def _scheduled_rights_check(self):
        """Periodic rights/license check"""
        while self.status in [ServiceStatus.STARTING, ServiceStatus.RUNNING]:
            try:
                await asyncio.sleep(self.config.rights_check_interval)

                if self.config.demo_mode:
                    # Demo: Occasionally generate rights alerts
                    import random
                    if random.random() > 0.8:
                        await self.notification_service.send_alert(
                            create_rights_alert(
                                license_name="Sample License",
                                days_remaining=random.randint(5, 30),
                                cost="$500/year",
                                source_agent="Rights Agent"
                            )
                        )

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Rights check error: {e}")

    def get_status(self) -> Dict:
        """Get service status and statistics"""
        return {
            "status": self.status.value,
            "stats": self.stats,
            "watch_folders": self.folder_watcher.get_watch_folders(),
            "mam_connections": {
                name: conn.get_status()
                for name, conn in self.mam_connectors.items()
            },
            "active_jobs": len(self.active_jobs),
            "queue_size": self.processing_queue.qsize(),
            "completed_jobs": len(self.completed_jobs),
            "alerts": self.notification_service.get_stats()
        }

    def get_recent_activity(self, limit: int = 20) -> List[Dict]:
        """Get recent processing activity"""
        return [job.to_dict() for job in self.completed_jobs[-limit:]]

    def get_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recent alerts"""
        return [a.to_dict() for a in self.notification_service.get_alerts(limit)]

    def _save_state(self):
        """Save service state to file"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            state = {
                "stats": self.stats,
                "completed_jobs": [job.to_dict() for job in self.completed_jobs[-50:]]
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")


# Convenience function to create and start service
async def start_autonomous_service(config: Optional[ServiceConfig] = None) -> AutonomousService:
    """Create and start the autonomous service"""
    service = AutonomousService(config)
    await service.start()
    return service
