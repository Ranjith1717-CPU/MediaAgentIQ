"""
MediaAgentIQ - Autonomous Agent Orchestrator

This module provides the autonomous execution layer for all agents:
- Background task processing
- Scheduled/periodic agent execution
- Event-driven triggers
- Multi-agent workflow coordination
- Real-time monitoring

Agents can run autonomously without user intervention.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from collections import deque
import uuid
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1  # Compliance violations, breaking news
    HIGH = 2      # Expiring licenses, trending alerts
    NORMAL = 3    # Regular processing
    LOW = 4       # Background optimization


class AgentType(Enum):
    """Available agent types."""
    # Original 8 agents
    CAPTION = "caption"
    CLIP = "clip"
    ARCHIVE = "archive"
    COMPLIANCE = "compliance"
    SOCIAL = "social"
    LOCALIZATION = "localization"
    RIGHTS = "rights"
    TRENDING = "trending"
    # Future-Ready agents (market gaps)
    DEEPFAKE_DETECTION = "deepfake_detection"
    LIVE_FACT_CHECK = "live_fact_check"
    AUDIENCE_INTELLIGENCE = "audience_intelligence"
    AI_PRODUCTION_DIRECTOR = "ai_production_director"
    BRAND_SAFETY = "brand_safety"
    CARBON_INTELLIGENCE = "carbon_intelligence"
    # Phase 1 Pipeline agents (broadcast pipeline gaps)
    INGEST_TRANSCODE = "ingest_transcode"
    SIGNAL_QUALITY = "signal_quality"
    PLAYOUT_SCHEDULING = "playout_scheduling"
    OTT_DISTRIBUTION = "ott_distribution"
    NEWSROOM_INTEGRATION = "newsroom_integration"


@dataclass
class Task:
    """Represents a task to be executed by an agent."""
    id: str
    agent_type: AgentType
    input_data: Any
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    callback: Optional[Callable] = None
    triggered_by: Optional[str] = None  # ID of task that triggered this one

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "agent_type": self.agent_type.value,
            "priority": self.priority.name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "has_result": self.result is not None,
            "error": self.error,
            "triggered_by": self.triggered_by
        }


@dataclass
class ScheduledJob:
    """Represents a scheduled recurring job."""
    id: str
    agent_type: AgentType
    input_data: Any
    interval_seconds: int
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "agent_type": self.agent_type.value,
            "interval_seconds": self.interval_seconds,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count
        }


class EventType(Enum):
    """Types of events that can trigger agents."""
    NEW_CONTENT = "new_content"           # New content uploaded
    COMPLIANCE_ALERT = "compliance_alert" # Compliance issue detected
    TRENDING_SPIKE = "trending_spike"     # Topic trending
    LICENSE_EXPIRING = "license_expiring" # License about to expire
    VIOLATION_DETECTED = "violation_detected"  # Unauthorized usage
    CAPTION_COMPLETE = "caption_complete" # Captions ready
    CLIP_DETECTED = "clip_detected"       # Viral clip found
    BREAKING_NEWS = "breaking_news"       # Breaking news alert


@dataclass
class Event:
    """Represents an event that can trigger agents."""
    type: EventType
    data: Dict
    timestamp: datetime = field(default_factory=datetime.now)
    source_agent: Optional[str] = None


class AgentOrchestrator:
    """
    Autonomous Agent Orchestrator

    Manages all agents and provides:
    - Background task queue processing
    - Scheduled periodic execution
    - Event-driven agent triggering
    - Multi-agent workflow coordination
    """

    def __init__(self):
        self.agents: Dict[AgentType, Any] = {}
        self.task_queue: deque = deque()
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: deque = deque(maxlen=1000)
        self.scheduled_jobs: Dict[str, ScheduledJob] = {}
        self.event_handlers: Dict[EventType, List[Callable]] = {et: [] for et in EventType}

        self._running = False
        self._worker_task: Optional[asyncio.Task] = None
        self._scheduler_task: Optional[asyncio.Task] = None
        self._monitor_task: Optional[asyncio.Task] = None

        # Statistics
        self.stats = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "events_triggered": 0,
            "uptime_start": None
        }

        # Event subscriptions (which agents listen to which events)
        self.event_subscriptions = {
            # Original subscriptions
            EventType.NEW_CONTENT: [
                AgentType.CAPTION, AgentType.CLIP, AgentType.COMPLIANCE, AgentType.ARCHIVE,
                # Future-Ready: scan all new content for deepfakes + brand safety
                AgentType.DEEPFAKE_DETECTION, AgentType.BRAND_SAFETY,
                # Future-Ready: start audience prediction for new content
                AgentType.AUDIENCE_INTELLIGENCE,
            ],
            EventType.CAPTION_COMPLETE: [
                AgentType.LOCALIZATION, AgentType.SOCIAL,
                # Future-Ready: fact-check captions as they arrive
                AgentType.LIVE_FACT_CHECK,
            ],
            EventType.CLIP_DETECTED: [AgentType.SOCIAL],
            EventType.COMPLIANCE_ALERT: [AgentType.SOCIAL],
            EventType.TRENDING_SPIKE: [AgentType.SOCIAL, AgentType.ARCHIVE],
            EventType.LICENSE_EXPIRING: [AgentType.RIGHTS],
            EventType.VIOLATION_DETECTED: [AgentType.RIGHTS],
            EventType.BREAKING_NEWS: [
                AgentType.SOCIAL, AgentType.TRENDING,
                # Future-Ready: production director handles live breaking coverage
                AgentType.AI_PRODUCTION_DIRECTOR,
                # Future-Ready: fact-check breaking news claims immediately
                AgentType.LIVE_FACT_CHECK,
            ],
        }

        logger.info("AgentOrchestrator initialized")

    def register_agent(self, agent_type: AgentType, agent: Any) -> None:
        """Register an agent with the orchestrator."""
        self.agents[agent_type] = agent
        logger.info(f"Registered agent: {agent_type.value}")

    def register_all_agents(self) -> None:
        """Register all available agents - original 8 + 6 future-ready."""
        from agents import (
            # Original 8
            CaptionAgent, ClipAgent, ArchiveAgent, ComplianceAgent,
            SocialPublishingAgent, LocalizationAgent, RightsAgent, TrendingAgent,
            # Future-Ready 6
            DeepfakeDetectionAgent, LiveFactCheckAgent, AudienceIntelligenceAgent,
            AIProductionDirectorAgent, BrandSafetyAgent, CarbonIntelligenceAgent,
        )

        # Original agents
        self.register_agent(AgentType.CAPTION, CaptionAgent())
        self.register_agent(AgentType.CLIP, ClipAgent())
        self.register_agent(AgentType.ARCHIVE, ArchiveAgent())
        self.register_agent(AgentType.COMPLIANCE, ComplianceAgent())
        self.register_agent(AgentType.SOCIAL, SocialPublishingAgent())
        self.register_agent(AgentType.LOCALIZATION, LocalizationAgent())
        self.register_agent(AgentType.RIGHTS, RightsAgent())
        self.register_agent(AgentType.TRENDING, TrendingAgent())

        # Future-Ready agents
        self.register_agent(AgentType.DEEPFAKE_DETECTION, DeepfakeDetectionAgent())
        self.register_agent(AgentType.LIVE_FACT_CHECK, LiveFactCheckAgent())
        self.register_agent(AgentType.AUDIENCE_INTELLIGENCE, AudienceIntelligenceAgent())
        self.register_agent(AgentType.AI_PRODUCTION_DIRECTOR, AIProductionDirectorAgent())
        self.register_agent(AgentType.BRAND_SAFETY, BrandSafetyAgent())
        self.register_agent(AgentType.CARBON_INTELLIGENCE, CarbonIntelligenceAgent())

        # Phase 1 Pipeline agents
        from agents.ingest_transcode_agent import IngestTranscodeAgent
        from agents.signal_quality_agent import SignalQualityAgent
        from agents.playout_scheduling_agent import PlayoutSchedulingAgent
        from agents.ott_distribution_agent import OTTDistributionAgent
        from agents.newsroom_integration_agent import NewsroomIntegrationAgent

        self.register_agent(AgentType.INGEST_TRANSCODE, IngestTranscodeAgent())
        self.register_agent(AgentType.SIGNAL_QUALITY, SignalQualityAgent())
        self.register_agent(AgentType.PLAYOUT_SCHEDULING, PlayoutSchedulingAgent())
        self.register_agent(AgentType.OTT_DISTRIBUTION, OTTDistributionAgent())
        self.register_agent(AgentType.NEWSROOM_INTEGRATION, NewsroomIntegrationAgent())

        logger.info("All 19 agents registered (8 original + 6 future-ready + 5 Phase 1 pipeline)")

    # ==================== Task Management ====================

    def submit_task(
        self,
        agent_type: AgentType,
        input_data: Any,
        priority: TaskPriority = TaskPriority.NORMAL,
        callback: Optional[Callable] = None,
        triggered_by: Optional[str] = None
    ) -> str:
        """
        Submit a task to the queue for processing.

        Args:
            agent_type: Which agent should process this
            input_data: Input for the agent
            priority: Task priority
            callback: Optional callback when complete
            triggered_by: ID of triggering task (for chains)

        Returns:
            Task ID
        """
        task = Task(
            id=str(uuid.uuid4())[:8],
            agent_type=agent_type,
            input_data=input_data,
            priority=priority,
            callback=callback,
            triggered_by=triggered_by
        )

        # Insert based on priority
        inserted = False
        for i, t in enumerate(self.task_queue):
            if task.priority.value < t.priority.value:
                self.task_queue.insert(i, task)
                inserted = True
                break

        if not inserted:
            self.task_queue.append(task)

        logger.info(f"Task {task.id} submitted: {agent_type.value} (priority: {priority.name})")
        return task.id

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get status of a task."""
        # Check running tasks
        if task_id in self.running_tasks:
            return self.running_tasks[task_id].to_dict()

        # Check queue
        for task in self.task_queue:
            if task.id == task_id:
                return task.to_dict()

        # Check completed
        for task in self.completed_tasks:
            if task.id == task_id:
                return task.to_dict()

        return None

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task."""
        for i, task in enumerate(self.task_queue):
            if task.id == task_id:
                task.status = TaskStatus.CANCELLED
                self.task_queue.remove(task)
                self.completed_tasks.append(task)
                logger.info(f"Task {task_id} cancelled")
                return True
        return False

    # ==================== Scheduled Jobs ====================

    def schedule_job(
        self,
        agent_type: AgentType,
        input_data: Any,
        interval_seconds: int,
        job_id: Optional[str] = None
    ) -> str:
        """
        Schedule a recurring job.

        Args:
            agent_type: Which agent to run
            input_data: Input for the agent
            interval_seconds: How often to run (in seconds)
            job_id: Optional custom job ID

        Returns:
            Job ID
        """
        job = ScheduledJob(
            id=job_id or str(uuid.uuid4())[:8],
            agent_type=agent_type,
            input_data=input_data,
            interval_seconds=interval_seconds,
            next_run=datetime.now()
        )

        self.scheduled_jobs[job.id] = job
        logger.info(f"Scheduled job {job.id}: {agent_type.value} every {interval_seconds}s")
        return job.id

    def setup_default_schedules(self) -> None:
        """Set up default scheduled jobs for autonomous operation."""

        # Trending Agent - Check trends every 5 minutes
        self.schedule_job(
            AgentType.TRENDING,
            {"mode": "monitor"},
            interval_seconds=300,  # 5 minutes
            job_id="trending_monitor"
        )

        # Compliance Agent - Continuous monitoring every 10 minutes
        self.schedule_job(
            AgentType.COMPLIANCE,
            {"mode": "monitor"},
            interval_seconds=600,  # 10 minutes
            job_id="compliance_monitor"
        )

        # Rights Agent - Check licenses every hour
        self.schedule_job(
            AgentType.RIGHTS,
            {"mode": "check_expiring"},
            interval_seconds=3600,  # 1 hour
            job_id="rights_monitor"
        )

        # Archive Agent - Index optimization every 6 hours
        self.schedule_job(
            AgentType.ARCHIVE,
            {"mode": "optimize"},
            interval_seconds=21600,  # 6 hours
            job_id="archive_optimize"
        )

        # ========== Future-Ready Agent Schedules ==========

        # Deepfake Detection - Scan all incoming content every 2 minutes
        self.schedule_job(
            AgentType.DEEPFAKE_DETECTION,
            {"mode": "monitor_incoming"},
            interval_seconds=120,  # 2 minutes
            job_id="deepfake_monitor"
        )

        # Live Fact-Check - Check live broadcast transcript every 3 minutes
        self.schedule_job(
            AgentType.LIVE_FACT_CHECK,
            {"mode": "live_monitor"},
            interval_seconds=180,  # 3 minutes
            job_id="fact_check_live"
        )

        # Audience Intelligence - Update retention predictions every 5 minutes
        self.schedule_job(
            AgentType.AUDIENCE_INTELLIGENCE,
            {"mode": "live_prediction"},
            interval_seconds=300,  # 5 minutes
            job_id="audience_live"
        )

        # AI Production Director - Refresh production cues every minute (live)
        self.schedule_job(
            AgentType.AI_PRODUCTION_DIRECTOR,
            {"mode": "live_assist"},
            interval_seconds=60,  # 1 minute
            job_id="production_director_live"
        )

        # Brand Safety - Score each segment every 2 minutes for ad decisions
        self.schedule_job(
            AgentType.BRAND_SAFETY,
            {"mode": "segment_scan"},
            interval_seconds=120,  # 2 minutes
            job_id="brand_safety_monitor"
        )

        # Carbon Intelligence - Update energy/carbon metrics every 30 minutes
        self.schedule_job(
            AgentType.CARBON_INTELLIGENCE,
            {"mode": "live_monitoring"},
            interval_seconds=1800,  # 30 minutes
            job_id="carbon_monitor"
        )

        # ========== Phase 1 Pipeline Agent Schedules ==========

        # Signal Quality — monitor live streams every 2 minutes
        self.schedule_job(
            AgentType.SIGNAL_QUALITY,
            {"mode": "live_monitor"},
            interval_seconds=120,
            job_id="signal_quality_monitor"
        )

        # Newsroom Integration — sync rundown every 3 minutes
        self.schedule_job(
            AgentType.NEWSROOM_INTEGRATION,
            {"mode": "sync"},
            interval_seconds=180,
            job_id="newsroom_sync"
        )

        # Playout Scheduling — refresh schedule every 5 minutes
        self.schedule_job(
            AgentType.PLAYOUT_SCHEDULING,
            {"mode": "schedule"},
            interval_seconds=300,
            job_id="playout_refresh"
        )

        # OTT Distribution — check CDN health every 10 minutes
        self.schedule_job(
            AgentType.OTT_DISTRIBUTION,
            {"mode": "health_check"},
            interval_seconds=600,
            job_id="ott_health"
        )

        logger.info("Default schedules configured (4 original + 6 future-ready + 4 Phase 1 pipeline)")

    def pause_job(self, job_id: str) -> bool:
        """Pause a scheduled job."""
        if job_id in self.scheduled_jobs:
            self.scheduled_jobs[job_id].enabled = False
            logger.info(f"Job {job_id} paused")
            return True
        return False

    def resume_job(self, job_id: str) -> bool:
        """Resume a paused job."""
        if job_id in self.scheduled_jobs:
            self.scheduled_jobs[job_id].enabled = True
            self.scheduled_jobs[job_id].next_run = datetime.now()
            logger.info(f"Job {job_id} resumed")
            return True
        return False

    # ==================== Event System ====================

    def emit_event(self, event: Event) -> None:
        """
        Emit an event that may trigger agents.

        Args:
            event: The event to emit
        """
        logger.info(f"Event emitted: {event.type.value} from {event.source_agent}")
        self.stats["events_triggered"] += 1

        # Get subscribed agents
        subscribed_agents = self.event_subscriptions.get(event.type, [])

        for agent_type in subscribed_agents:
            # Create task for each subscribed agent
            self.submit_task(
                agent_type=agent_type,
                input_data={"event": event.type.value, "event_data": event.data},
                priority=TaskPriority.HIGH if event.type in [
                    EventType.COMPLIANCE_ALERT,
                    EventType.BREAKING_NEWS,
                    EventType.VIOLATION_DETECTED
                ] else TaskPriority.NORMAL,
                triggered_by=f"event:{event.type.value}"
            )

        # Call registered handlers
        for handler in self.event_handlers.get(event.type, []):
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Event handler error: {e}")

    def on_event(self, event_type: EventType, handler: Callable) -> None:
        """Register an event handler."""
        self.event_handlers[event_type].append(handler)

    # ==================== Workflow Chains ====================

    def submit_workflow(
        self,
        workflow_name: str,
        input_data: Any,
        agent_sequence: List[AgentType]
    ) -> str:
        """
        Submit a multi-agent workflow.

        Agents run in sequence, each receiving output from the previous.

        Args:
            workflow_name: Name for this workflow
            input_data: Initial input
            agent_sequence: List of agents to run in order

        Returns:
            Workflow ID (first task ID)
        """
        if not agent_sequence:
            return None

        workflow_id = str(uuid.uuid4())[:8]
        logger.info(f"Workflow {workflow_id} ({workflow_name}): {[a.value for a in agent_sequence]}")

        # Submit first task
        first_task_id = self.submit_task(
            agent_type=agent_sequence[0],
            input_data=input_data,
            priority=TaskPriority.NORMAL
        )

        # Store remaining sequence for chaining
        self._workflow_chains[workflow_id] = {
            "remaining": agent_sequence[1:],
            "current_task": first_task_id,
            "results": []
        }

        return workflow_id

    # ==================== Background Workers ====================

    async def _process_task(self, task: Task) -> None:
        """Process a single task."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        self.running_tasks[task.id] = task

        try:
            agent = self.agents.get(task.agent_type)
            if not agent:
                raise ValueError(f"Agent not found: {task.agent_type}")

            # Execute agent
            result = await agent.process(task.input_data)

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            self.stats["tasks_processed"] += 1

            logger.info(f"Task {task.id} completed: {task.agent_type.value}")

            # Emit events based on results
            await self._handle_task_completion(task)

            # Execute callback if provided
            if task.callback:
                try:
                    task.callback(task)
                except Exception as e:
                    logger.error(f"Callback error for task {task.id}: {e}")

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            self.stats["tasks_failed"] += 1
            logger.error(f"Task {task.id} failed: {e}")

        finally:
            del self.running_tasks[task.id]
            self.completed_tasks.append(task)

    async def _handle_task_completion(self, task: Task) -> None:
        """Handle task completion and emit appropriate events."""
        if not task.result or not task.result.get("success"):
            return

        data = task.result.get("data", {})

        # Caption complete -> trigger localization/social
        if task.agent_type == AgentType.CAPTION:
            self.emit_event(Event(
                type=EventType.CAPTION_COMPLETE,
                data={"captions": data},
                source_agent="caption"
            ))

        # Clip detected -> trigger social
        elif task.agent_type == AgentType.CLIP:
            if data.get("viral_moments"):
                self.emit_event(Event(
                    type=EventType.CLIP_DETECTED,
                    data={"clips": data["viral_moments"]},
                    source_agent="clip"
                ))

        # Compliance issue -> alert
        elif task.agent_type == AgentType.COMPLIANCE:
            issues = data.get("issues", [])
            critical = [i for i in issues if i.get("severity") == "critical"]
            if critical:
                self.emit_event(Event(
                    type=EventType.COMPLIANCE_ALERT,
                    data={"issues": critical},
                    source_agent="compliance"
                ))

        # Trending spike
        elif task.agent_type == AgentType.TRENDING:
            trends = data.get("trends", [])
            hot_trends = [t for t in trends if t.get("velocity_score", 0) > 90]
            if hot_trends:
                self.emit_event(Event(
                    type=EventType.TRENDING_SPIKE,
                    data={"trends": hot_trends},
                    source_agent="trending"
                ))

            breaking = data.get("breaking_news", [])
            if breaking:
                self.emit_event(Event(
                    type=EventType.BREAKING_NEWS,
                    data={"news": breaking},
                    source_agent="trending"
                ))

        # Rights violations
        elif task.agent_type == AgentType.RIGHTS:
            violations = data.get("violations", [])
            if violations:
                self.emit_event(Event(
                    type=EventType.VIOLATION_DETECTED,
                    data={"violations": violations},
                    source_agent="rights"
                ))

            expiring = data.get("expiring_soon", [])
            critical_expiring = [l for l in expiring if l.get("days_until_expiry", 999) < 30]
            if critical_expiring:
                self.emit_event(Event(
                    type=EventType.LICENSE_EXPIRING,
                    data={"licenses": critical_expiring},
                    source_agent="rights"
                ))

    async def _task_worker(self) -> None:
        """Background worker that processes tasks from the queue."""
        logger.info("Task worker started")

        while self._running:
            if self.task_queue:
                task = self.task_queue.popleft()
                await self._process_task(task)
            else:
                await asyncio.sleep(0.1)  # Small sleep when queue is empty

        logger.info("Task worker stopped")

    async def _scheduler_worker(self) -> None:
        """Background worker that runs scheduled jobs."""
        logger.info("Scheduler worker started")

        while self._running:
            now = datetime.now()

            for job_id, job in self.scheduled_jobs.items():
                if not job.enabled:
                    continue

                if job.next_run and now >= job.next_run:
                    # Submit task for this job
                    self.submit_task(
                        agent_type=job.agent_type,
                        input_data=job.input_data,
                        priority=TaskPriority.NORMAL,
                        triggered_by=f"schedule:{job_id}"
                    )

                    job.last_run = now
                    job.next_run = now + timedelta(seconds=job.interval_seconds)
                    job.run_count += 1

                    logger.info(f"Scheduled job {job_id} triggered (run #{job.run_count})")

            await asyncio.sleep(1)  # Check every second

        logger.info("Scheduler worker stopped")

    async def _monitor_worker(self) -> None:
        """Background worker that monitors system health."""
        logger.info("Monitor worker started")

        while self._running:
            # Log stats every minute
            await asyncio.sleep(60)

            if self._running:
                logger.info(
                    f"Orchestrator stats: "
                    f"queue={len(self.task_queue)}, "
                    f"running={len(self.running_tasks)}, "
                    f"processed={self.stats['tasks_processed']}, "
                    f"failed={self.stats['tasks_failed']}, "
                    f"events={self.stats['events_triggered']}"
                )

        logger.info("Monitor worker stopped")

    # ==================== Orchestrator Control ====================

    async def start(self) -> None:
        """Start the orchestrator and all background workers."""
        if self._running:
            logger.warning("Orchestrator already running")
            return

        self._running = True
        self.stats["uptime_start"] = datetime.now()
        self._workflow_chains = {}

        # Start background workers
        self._worker_task = asyncio.create_task(self._task_worker())
        self._scheduler_task = asyncio.create_task(self._scheduler_worker())
        self._monitor_task = asyncio.create_task(self._monitor_worker())

        logger.info("🚀 Orchestrator started - Agents running autonomously")

    async def stop(self) -> None:
        """Stop the orchestrator gracefully."""
        if not self._running:
            return

        logger.info("Stopping orchestrator...")
        self._running = False

        # Wait for workers to finish
        if self._worker_task:
            await self._worker_task
        if self._scheduler_task:
            await self._scheduler_task
        if self._monitor_task:
            await self._monitor_task

        logger.info("Orchestrator stopped")

    def get_status(self) -> Dict:
        """Get orchestrator status."""
        uptime = None
        if self.stats["uptime_start"]:
            uptime = (datetime.now() - self.stats["uptime_start"]).total_seconds()

        return {
            "running": self._running,
            "uptime_seconds": uptime,
            "queue_size": len(self.task_queue),
            "running_tasks": len(self.running_tasks),
            "scheduled_jobs": len(self.scheduled_jobs),
            "registered_agents": list(self.agents.keys()),
            "stats": self.stats
        }

    def get_queue(self) -> List[Dict]:
        """Get current task queue."""
        return [t.to_dict() for t in self.task_queue]

    def get_scheduled_jobs(self) -> List[Dict]:
        """Get scheduled jobs."""
        return [j.to_dict() for j in self.scheduled_jobs.values()]


# ==================== Global Orchestrator Instance ====================

orchestrator = AgentOrchestrator()


# ==================== Convenience Functions ====================

async def start_autonomous_agents():
    """Start all agents running autonomously."""
    orchestrator.register_all_agents()
    orchestrator.setup_default_schedules()
    await orchestrator.start()
    return orchestrator


async def stop_autonomous_agents():
    """Stop autonomous agent execution."""
    await orchestrator.stop()


def submit_content_for_processing(file_path: str, run_all: bool = True) -> Dict[str, str]:
    """
    Submit new content for processing by agents.

    Args:
        file_path: Path to the content file
        run_all: If True, runs all relevant agents

    Returns:
        Dict of task IDs for each agent
    """
    task_ids = {}

    if run_all:
        # Submit to all content-processing agents
        task_ids["caption"] = orchestrator.submit_task(
            AgentType.CAPTION, file_path, TaskPriority.NORMAL
        )
        task_ids["clip"] = orchestrator.submit_task(
            AgentType.CLIP, file_path, TaskPriority.NORMAL
        )
        task_ids["compliance"] = orchestrator.submit_task(
            AgentType.COMPLIANCE, {"file": file_path}, TaskPriority.HIGH
        )
        task_ids["archive"] = orchestrator.submit_task(
            AgentType.ARCHIVE, {"file": file_path, "mode": "index"}, TaskPriority.LOW
        )

        # Future-Ready: Run deepfake scan on new content (CRITICAL priority)
        task_ids["deepfake"] = orchestrator.submit_task(
            AgentType.DEEPFAKE_DETECTION, {"file": file_path}, TaskPriority.CRITICAL
        )
        # Future-Ready: Score brand safety before ad insertion decisions
        task_ids["brand_safety"] = orchestrator.submit_task(
            AgentType.BRAND_SAFETY, {"file": file_path}, TaskPriority.HIGH
        )
        # Future-Ready: Start audience prediction for this content
        task_ids["audience"] = orchestrator.submit_task(
            AgentType.AUDIENCE_INTELLIGENCE, {"file": file_path}, TaskPriority.NORMAL
        )

    # Emit event to trigger event-subscribed agents
    orchestrator.emit_event(Event(
        type=EventType.NEW_CONTENT,
        data={"file_path": file_path},
        source_agent="system"
    ))

    return task_ids


# ==================== CLI Entry Point ====================

if __name__ == "__main__":
    import sys

    async def main():
        print("=" * 60)
        print("MediaAgentIQ - Autonomous Agent Orchestrator")
        print("=" * 60)

        # Start orchestrator
        await start_autonomous_agents()

        print("\n✅ All 14 agents are now running autonomously! (8 original + 6 future-ready)")
        print("\nScheduled Jobs:")
        for job in orchestrator.get_scheduled_jobs():
            print(f"  - {job['agent_type']}: every {job['interval_seconds']}s")

        print("\nPress Ctrl+C to stop...")

        try:
            # Keep running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            await stop_autonomous_agents()
            print("Goodbye!")

    asyncio.run(main())
