"""
MediaAgentIQ — Persistent Agent Memory Layer

Provides per-agent .md memory files that accumulate knowledge over time.
Each agent gets its own file in memory/agents/.

Shared files:
  - inter_agent_comms.md : cross-agent event log
  - task_history.md      : compact global audit trail (table rows)
  - system_state.md      : orchestrator snapshot (fully rewritten each interval)

Concurrency safety: all file I/O is synchronous (Path.read_text / write_text).
asyncio is single-threaded — no await between read and write, so no interleaving.
No locks needed.
"""

import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from settings import Settings

logger = logging.getLogger(__name__)

# Separator between sections in .md files
_SEP = "\n\n---\n\n"

# High-value output keys per agent slug → list of keys to extract from result["data"]
_OUTPUT_KEY_MAP: Dict[str, List[str]] = {
    "caption_agent":               ["segments", "qa_issues", "confidence_avg", "word_count"],
    "clip_agent":                  ["viral_moments", "clip_count", "top_score", "duration_s"],
    "archive_agent":               ["indexed_items", "categories", "storage_used_mb", "retrieval_score"],
    "compliance_agent":            ["issues", "violations", "score", "critical_count"],
    "social_publishing_agent":     ["posts_scheduled", "platforms", "reach_estimate", "engagement_score"],
    "localization_agent":          ["languages", "segments_localized", "confidence_avg", "translation_pairs"],
    "rights_agent":                ["licenses", "violations", "expiring_soon", "cleared_pct"],
    "trending_agent":              ["trends", "breaking_news", "velocity_score", "top_topic"],
    "deepfake_detection_agent":    ["risk_score", "verdict", "layers_checked", "confidence"],
    "live_fact_check_agent":       ["claims_checked", "false_claims", "confidence", "databases_queried"],
    "audience_intelligence_agent": ["retention_curve", "drop_off_risk", "engagement_score", "demographic_bands"],
    "ai_production_director_agent":["shots_planned", "lower_thirds", "rundown_changes", "auto_accepted"],
    "brand_safety_agent":          ["safety_score", "garm_flags", "cpm_modifier", "advertiser_profiles"],
    "carbon_intelligence_agent":   ["carbon_footprint_kg", "scope", "esg_score", "renewable_pct"],
    "ingest_transcode_agent":      ["profiles", "output_files", "duration_s", "bitrate_kbps"],
    "signal_quality_agent":        ["loudness_lufs", "true_peak_dbtp", "issues", "compliance_status"],
    "playout_scheduling_agent":    ["items_scheduled", "next_item", "gaps_found", "on_air_confidence"],
    "ott_distribution_agent":      ["streams_active", "cdn_health", "bitrate_avg_mbps", "viewer_count"],
    "newsroom_integration_agent":  ["rundown_items", "sync_status", "stories_updated", "breaking_count"],
}

# Fixed 5-line header for task_history.md
_TASK_HISTORY_HEADER = (
    "# Task History — Global Audit Log\n"
    "_Compact per-task log across all agents_\n\n"
    "| Timestamp | Agent | Task ID | Status | Duration |\n"
    "|-----------|-------|---------|--------|----------|\n"
)


class AgentMemoryLayer:
    """
    Persistent .md memory for a single agent.

    One instance per agent, created in BaseAgent.__init__ when MEMORY_ENABLED=True.
    Call load() once after construction to create files and warm the context cache.
    """

    def __init__(self, agent_name: str, settings: "Settings") -> None:
        self._agent_name = agent_name
        self._settings = settings

        # Slug: lowercase, spaces → underscore, strip non-alphanumeric/underscore
        slug = re.sub(r"[^a-z0-9_]", "", agent_name.lower().replace(" ", "_"))
        self._slug = slug

        # Paths
        agents_dir = Path(settings.MEMORY_DIR) / "agents"
        self._agent_file = agents_dir / f"{slug}.md"
        self._inter_agent_file = agents_dir / "inter_agent_comms.md"
        self._task_history_file = agents_dir / "task_history.md"

        # Cache of recent entry strings (populated by load(), updated on save)
        self._recent_context: List[str] = []

    # ==================== Public API ====================

    def load(self) -> None:
        """Create agent file if missing; warm the recent-context cache."""
        self._agent_file.parent.mkdir(parents=True, exist_ok=True)

        if not self._agent_file.exists():
            self._agent_file.write_text(
                self._make_agent_header(entries=0, success_pct=None, avg_ms=None),
                encoding="utf-8",
            )
            logger.debug(f"Memory: created {self._agent_file.name}")

        content = self._agent_file.read_text(encoding="utf-8")
        self._recent_context = self._parse_recent_entries(
            content, self._settings.MEMORY_RECENT_CONTEXT_ENTRIES
        )

    def save_task(
        self,
        task_id: str,
        input_data: Any,
        result: Dict[str, Any],
        duration_ms: float,
        triggered_events: List[Tuple[str, List[str]]],
    ) -> None:
        """Append a task entry to the agent's .md file and to task_history.md."""
        success = bool(result.get("success"))
        mode = result.get("mode", "demo")
        status_str = "SUCCESS" if success else "FAILURE"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        input_summary = self._summarize_input(input_data)
        output_summary = self._summarize_output(result)

        lines = [
            f"## [{ts}] Task `{task_id}` {status_str} ({mode})",
            f"**Input**: `{input_summary}`",
            f"**Output**: {output_summary}",
        ]
        if triggered_events:
            trig_str = ", ".join(
                f"{et} → {', '.join(subs)}" for et, subs in triggered_events
            )
            lines.append(f"**Triggered**: {trig_str}")
        lines.append(f"**Duration**: {int(duration_ms)}ms")

        entry = "\n".join(lines)

        content = self._agent_file.read_text(encoding="utf-8")
        content = content + _SEP + entry
        content = self._trim_if_needed(
            content,
            self._settings.MEMORY_MAX_ENTRIES_PER_AGENT,
            self._settings.MEMORY_TRIM_TO,
        )
        content = self._update_agent_header(content)
        self._agent_file.write_text(content, encoding="utf-8")

        # Refresh cache
        self._recent_context = self._parse_recent_entries(
            content, self._settings.MEMORY_RECENT_CONTEXT_ENTRIES
        )

        self._append_task_history(task_id, ts, status_str, duration_ms)

    def update_last_entry_triggered(
        self, triggered_events: List[Tuple[str, List[str]]]
    ) -> None:
        """
        Patch the last entry with a **Triggered** line.
        Called by the orchestrator after events have fired.
        """
        if not triggered_events:
            return

        content = self._agent_file.read_text(encoding="utf-8")
        parts = content.split(_SEP)
        if len(parts) < 2:
            return  # No entries yet

        trig_str = ", ".join(
            f"{et} → {', '.join(subs)}" for et, subs in triggered_events
        )
        triggered_line = f"**Triggered**: {trig_str}"

        last_entry = parts[-1]
        if "**Triggered**:" in last_entry:
            last_entry = re.sub(r"\*\*Triggered\*\*:.*", triggered_line, last_entry)
        else:
            last_entry = last_entry.replace(
                "**Duration**:", f"{triggered_line}\n**Duration**:"
            )

        parts[-1] = last_entry
        self._agent_file.write_text(_SEP.join(parts), encoding="utf-8")

    def log_inter_agent_event(
        self,
        event_type: str,
        source_agent: str,
        source_task_id: str,
        subscribers: List[str],
        payload_summary: str,
        tasks_queued: int,
    ) -> None:
        """Append an event entry to the shared inter_agent_comms.md."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sub_str = ", ".join(subscribers) if subscribers else "none"

        entry = (
            f"## [{ts}] {event_type}\n"
            f"**Source**: {source_agent} (task `{source_task_id}`)\n"
            f"**Subscribers**: {sub_str}\n"
            f"**Payload summary**: {payload_summary}\n"
            f"**Tasks queued**: {tasks_queued}"
        )

        if not self._inter_agent_file.exists():
            self._inter_agent_file.write_text(
                "# Inter-Agent Communications Log\n"
                "_Last updated: N/A | Events: 0_",
                encoding="utf-8",
            )

        content = self._inter_agent_file.read_text(encoding="utf-8")
        content = content + _SEP + entry

        # Trim if needed
        max_e = self._settings.MEMORY_INTER_AGENT_MAX_ENTRIES
        trim_to = max(max_e - 200, 100)
        content = self._trim_if_needed(content, max_e, trim_to)

        # Update header: event count
        parts = content.split(_SEP)
        event_count = len(parts) - 1
        header_lines = parts[0].split("\n")
        new_stat = f"_Last updated: {ts} | Events: {event_count}_"
        if len(header_lines) >= 2:
            header_lines[1] = new_stat
        else:
            header_lines.append(new_stat)
        parts[0] = "\n".join(header_lines)

        self._inter_agent_file.write_text(_SEP.join(parts), encoding="utf-8")

    def get_agent_stats(self) -> Dict[str, Any]:
        """Read header line O(1) for entries / success_rate / avg_duration."""
        if not self._agent_file.exists():
            return {"entries": 0, "success_rate_pct": None, "avg_duration_ms": None}
        content = self._agent_file.read_text(encoding="utf-8")
        return self._parse_header_stats(content)

    def get_memory_context_prompt(self) -> str:
        """Return last N entries formatted as a LLM system-prompt block."""
        if not self._recent_context:
            return ""
        lines = [f"# {self._agent_name} — Recent Memory\n"]
        for entry in self._recent_context:
            lines.append(entry.strip())
            lines.append("---")
        return "\n".join(lines)

    # ==================== Private Helpers ====================

    def _make_agent_header(
        self,
        entries: int,
        success_pct: Optional[float],
        avg_ms: Optional[float],
    ) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sr = f"{success_pct:.1f}%" if success_pct is not None else "N/A"
        ad = f"{int(avg_ms)}ms" if avg_ms is not None else "N/A"
        return (
            f"# {self._agent_name} — Memory Log\n"
            f"_Last updated: {ts} | Entries: {entries} | Success rate: {sr} | Avg duration: {ad}_"
        )

    def _update_agent_header(self, content: str) -> str:
        """Recount entries / success / avg-duration and rewrite header line 2."""
        parts = content.split(_SEP)
        entry_parts = [p for p in parts[1:] if p.strip()]
        n = len(entry_parts)

        successes = sum(1 for e in entry_parts if " SUCCESS " in e or e.lstrip().startswith("## [") and "SUCCESS" in e)
        success_pct = (successes / n * 100) if n > 0 else None

        durations = []
        for e in entry_parts:
            m = re.search(r"\*\*Duration\*\*:\s*(\d+)ms", e)
            if m:
                durations.append(int(m.group(1)))
        avg_ms = sum(durations) / len(durations) if durations else None

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sr = f"{success_pct:.1f}%" if success_pct is not None else "N/A"
        ad = f"{int(avg_ms)}ms" if avg_ms is not None else "N/A"
        new_stat_line = (
            f"_Last updated: {ts} | Entries: {n} | Success rate: {sr} | Avg duration: {ad}_"
        )

        header = parts[0]
        header_lines = header.split("\n")
        if len(header_lines) >= 2:
            header_lines[1] = new_stat_line
        else:
            header_lines.append(new_stat_line)
        parts[0] = "\n".join(header_lines)

        return _SEP.join(parts)

    def _parse_header_stats(self, content: str) -> Dict[str, Any]:
        """Parse entries / success_rate / avg_duration from header line 2."""
        lines = content.split("\n", 2)
        stats: Dict[str, Any] = {"entries": 0, "success_rate_pct": None, "avg_duration_ms": None}
        if len(lines) < 2:
            return stats
        stat_line = lines[1]
        m = re.search(r"Entries:\s*(\d+)", stat_line)
        if m:
            stats["entries"] = int(m.group(1))
        m = re.search(r"Success rate:\s*([\d.]+)%", stat_line)
        if m:
            stats["success_rate_pct"] = float(m.group(1))
        m = re.search(r"Avg duration:\s*(\d+)ms", stat_line)
        if m:
            stats["avg_duration_ms"] = int(m.group(1))
        return stats

    def _parse_recent_entries(self, content: str, n: int) -> List[str]:
        """Return last n entry strings (excluding header part)."""
        parts = content.split(_SEP)
        entries = [p for p in parts[1:] if p.strip()]
        return entries[-n:] if len(entries) >= n else entries

    def _trim_if_needed(self, content: str, max_entries: int, trim_to: int) -> str:
        """Keep newest trim_to entries if total exceeds max_entries."""
        parts = content.split(_SEP)
        header = parts[0]
        entries = [p for p in parts[1:] if p.strip()]
        if len(entries) > max_entries:
            entries = entries[-trim_to:]
        return _SEP.join([header] + entries)

    def _summarize_input(self, input_data: Any) -> str:
        """Produce a one-line summary of the input."""
        if isinstance(input_data, str):
            return input_data[:80]
        if isinstance(input_data, Path):
            return input_data.name
        if isinstance(input_data, dict):
            pairs = [f"{k}={str(v)[:20]}" for k, v in list(input_data.items())[:2]]
            return "{" + ", ".join(pairs) + "}"
        return repr(input_data)[:80]

    def _summarize_output(self, result: Dict[str, Any]) -> str:
        """Extract high-value facts from result using the agent-specific key map."""
        data = result.get("data") or {}
        if not isinstance(data, dict):
            return f"data={str(data)[:60]}"

        keys = _OUTPUT_KEY_MAP.get(self._slug)
        if not keys:
            # Fallback: first 4 scalar keys
            keys = [
                k for k, v in data.items()
                if isinstance(v, (str, int, float, bool))
            ][:4]

        parts = []
        for k in keys:
            val = data.get(k)
            if val is None:
                continue
            if isinstance(val, list):
                parts.append(f"{k}={len(val)}")
            elif isinstance(val, float):
                parts.append(f"{k}={val:.2f}")
            else:
                parts.append(f"{k}={val}")

        return ", ".join(parts) if parts else "no data"

    def _append_task_history(
        self, task_id: str, ts: str, status: str, duration_ms: float
    ) -> None:
        """Append a compact table row to the global task_history.md."""
        if not self._task_history_file.exists():
            self._task_history_file.write_text(_TASK_HISTORY_HEADER, encoding="utf-8")

        row = f"| {ts} | {self._slug} | `{task_id}` | {status} | {int(duration_ms)}ms |\n"
        content = self._task_history_file.read_text(encoding="utf-8") + row

        # Trim if over limit
        lines = content.splitlines()
        # Data rows are everything after the 4-line header
        data_rows = [l for l in lines[4:] if l.strip()]
        if len(data_rows) > self._settings.MEMORY_TASK_HISTORY_MAX_ENTRIES:
            keep = self._settings.MEMORY_TASK_HISTORY_MAX_ENTRIES - 500
            content = _TASK_HISTORY_HEADER + "\n".join(data_rows[-keep:]) + "\n"

        self._task_history_file.write_text(content, encoding="utf-8")
