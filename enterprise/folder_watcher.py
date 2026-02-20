"""
MediaAgentIQ - Folder Watcher Service

Monitors designated folders for new media assets and triggers agent processing.
Integrates with MAM watch folders, hot folders, and ingest directories.
"""

import os
import time
import asyncio
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger("folder_watcher")


class AssetType(Enum):
    """Supported media asset types"""
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    DOCUMENT = "document"
    UNKNOWN = "unknown"


# File extension mappings
EXTENSION_MAP = {
    # Video
    ".mp4": AssetType.VIDEO, ".mov": AssetType.VIDEO, ".avi": AssetType.VIDEO,
    ".mkv": AssetType.VIDEO, ".mxf": AssetType.VIDEO, ".wmv": AssetType.VIDEO,
    ".m4v": AssetType.VIDEO, ".webm": AssetType.VIDEO, ".mpg": AssetType.VIDEO,
    ".mpeg": AssetType.VIDEO, ".ts": AssetType.VIDEO, ".m2ts": AssetType.VIDEO,
    # Audio
    ".mp3": AssetType.AUDIO, ".wav": AssetType.AUDIO, ".aac": AssetType.AUDIO,
    ".flac": AssetType.AUDIO, ".m4a": AssetType.AUDIO, ".ogg": AssetType.AUDIO,
    ".wma": AssetType.AUDIO, ".aiff": AssetType.AUDIO,
    # Image
    ".jpg": AssetType.IMAGE, ".jpeg": AssetType.IMAGE, ".png": AssetType.IMAGE,
    ".gif": AssetType.IMAGE, ".bmp": AssetType.IMAGE, ".tiff": AssetType.IMAGE,
    # Document
    ".pdf": AssetType.DOCUMENT, ".doc": AssetType.DOCUMENT, ".docx": AssetType.DOCUMENT,
    ".srt": AssetType.DOCUMENT, ".vtt": AssetType.DOCUMENT, ".xml": AssetType.DOCUMENT,
}


@dataclass
class WatchConfig:
    """Configuration for a watched folder"""
    path: str
    name: str = ""
    enabled: bool = True
    recursive: bool = True
    file_types: List[str] = field(default_factory=lambda: ["video", "audio"])
    min_file_size_mb: float = 0.1  # Minimum file size to process
    stable_time_seconds: int = 5  # Wait for file to be stable before processing
    auto_archive: bool = False  # Move processed files to archive folder
    archive_path: Optional[str] = None
    trigger_agents: List[str] = field(default_factory=lambda: ["all"])  # Which agents to trigger
    priority: str = "normal"  # normal, high, critical
    metadata: Dict = field(default_factory=dict)  # Custom metadata for this watch folder

    def __post_init__(self):
        if not self.name:
            self.name = Path(self.path).name


@dataclass
class DetectedAsset:
    """Represents a detected asset in a watch folder"""
    path: str
    filename: str
    asset_type: AssetType
    size_bytes: int
    detected_at: datetime
    watch_config: WatchConfig
    file_hash: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    status: str = "detected"  # detected, processing, completed, failed

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)

    def to_dict(self) -> Dict:
        return {
            "path": self.path,
            "filename": self.filename,
            "asset_type": self.asset_type.value,
            "size_mb": round(self.size_mb, 2),
            "detected_at": self.detected_at.isoformat(),
            "watch_folder": self.watch_config.name,
            "status": self.status,
            "metadata": self.metadata
        }


class FolderWatcher:
    """
    Enterprise Folder Watcher Service

    Monitors multiple folders for new media assets and triggers
    automated agent processing. Integrates with MAM/PAM systems.

    Features:
    - Multi-folder monitoring with individual configurations
    - File stability detection (waits for uploads to complete)
    - Duplicate detection via file hashing
    - Automatic agent triggering
    - MAM metadata integration
    - Event callbacks for custom handling
    """

    def __init__(self, check_interval: int = 5):
        self.watch_configs: Dict[str, WatchConfig] = {}
        self.check_interval = check_interval
        self.running = False
        self.processed_files: Set[str] = set()  # Track processed files by hash
        self.pending_files: Dict[str, Dict] = {}  # Files waiting for stability

        # Callbacks
        self.on_asset_detected: Optional[Callable] = None
        self.on_asset_ready: Optional[Callable] = None
        self.on_processing_complete: Optional[Callable] = None
        self.on_error: Optional[Callable] = None

        # Statistics
        self.stats = {
            "total_detected": 0,
            "total_processed": 0,
            "total_failed": 0,
            "start_time": None,
            "last_check": None
        }

        # State file for persistence
        self.state_file = Path("enterprise/watcher_state.json")
        self._load_state()

        logger.info("FolderWatcher initialized")

    def add_watch_folder(self, config: WatchConfig) -> bool:
        """Add a folder to watch"""
        path = Path(config.path)

        if not path.exists():
            logger.warning(f"Watch folder does not exist: {config.path}")
            # Create the folder
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created watch folder: {config.path}")
            except Exception as e:
                logger.error(f"Failed to create watch folder: {e}")
                return False

        self.watch_configs[config.path] = config
        logger.info(f"Added watch folder: {config.name} ({config.path})")
        self._save_state()
        return True

    def remove_watch_folder(self, path: str) -> bool:
        """Remove a folder from watching"""
        if path in self.watch_configs:
            del self.watch_configs[path]
            logger.info(f"Removed watch folder: {path}")
            self._save_state()
            return True
        return False

    def get_watch_folders(self) -> List[Dict]:
        """Get list of all watch folders and their status"""
        folders = []
        for path, config in self.watch_configs.items():
            folder_info = {
                "path": path,
                "name": config.name,
                "enabled": config.enabled,
                "recursive": config.recursive,
                "file_types": config.file_types,
                "trigger_agents": config.trigger_agents,
                "priority": config.priority,
                "exists": Path(path).exists(),
                "file_count": self._count_files(path) if Path(path).exists() else 0
            }
            folders.append(folder_info)
        return folders

    def _count_files(self, path: str) -> int:
        """Count media files in a folder"""
        count = 0
        try:
            for ext in EXTENSION_MAP.keys():
                count += len(list(Path(path).glob(f"**/*{ext}")))
        except:
            pass
        return count

    def _get_file_hash(self, filepath: str, chunk_size: int = 8192) -> str:
        """Generate hash of file for duplicate detection"""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                # Only hash first and last chunks for speed on large files
                chunk = f.read(chunk_size)
                hasher.update(chunk)
                f.seek(-chunk_size, 2)  # Seek to end
                chunk = f.read(chunk_size)
                hasher.update(chunk)
                # Also include file size
                hasher.update(str(os.path.getsize(filepath)).encode())
            return hasher.hexdigest()
        except:
            return hashlib.md5(filepath.encode()).hexdigest()

    def _is_file_stable(self, filepath: str, wait_seconds: int) -> bool:
        """Check if file has stopped being written to"""
        if filepath not in self.pending_files:
            # First time seeing this file
            self.pending_files[filepath] = {
                "size": os.path.getsize(filepath),
                "first_seen": time.time(),
                "last_change": time.time()
            }
            return False

        current_size = os.path.getsize(filepath)
        pending = self.pending_files[filepath]

        if current_size != pending["size"]:
            # File is still being written
            pending["size"] = current_size
            pending["last_change"] = time.time()
            return False

        # Check if file has been stable long enough
        if time.time() - pending["last_change"] >= wait_seconds:
            del self.pending_files[filepath]
            return True

        return False

    def _detect_asset_type(self, filepath: str) -> AssetType:
        """Detect asset type from file extension"""
        ext = Path(filepath).suffix.lower()
        return EXTENSION_MAP.get(ext, AssetType.UNKNOWN)

    def _should_process_file(self, filepath: str, config: WatchConfig) -> bool:
        """Determine if a file should be processed"""
        path = Path(filepath)

        # Check file type
        asset_type = self._detect_asset_type(filepath)
        if asset_type == AssetType.UNKNOWN:
            return False

        if asset_type.value not in config.file_types:
            return False

        # Check file size
        try:
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if size_mb < config.min_file_size_mb:
                return False
        except:
            return False

        # Check if already processed
        file_hash = self._get_file_hash(filepath)
        if file_hash in self.processed_files:
            return False

        return True

    def scan_folder(self, config: WatchConfig) -> List[DetectedAsset]:
        """Scan a single folder for new assets"""
        detected = []
        path = Path(config.path)

        if not path.exists():
            return detected

        # Get all files
        pattern = "**/*" if config.recursive else "*"

        for filepath in path.glob(pattern):
            if not filepath.is_file():
                continue

            filepath_str = str(filepath)

            if not self._should_process_file(filepath_str, config):
                continue

            # Check file stability
            if not self._is_file_stable(filepath_str, config.stable_time_seconds):
                continue

            # Create detected asset
            asset = DetectedAsset(
                path=filepath_str,
                filename=filepath.name,
                asset_type=self._detect_asset_type(filepath_str),
                size_bytes=os.path.getsize(filepath_str),
                detected_at=datetime.now(),
                watch_config=config,
                file_hash=self._get_file_hash(filepath_str)
            )

            detected.append(asset)
            self.stats["total_detected"] += 1

            # Mark as processed
            self.processed_files.add(asset.file_hash)

            logger.info(f"Detected new asset: {asset.filename} ({asset.size_mb:.2f} MB)")

        return detected

    async def scan_all_folders(self) -> List[DetectedAsset]:
        """Scan all watch folders for new assets"""
        all_detected = []

        for path, config in self.watch_configs.items():
            if not config.enabled:
                continue

            detected = self.scan_folder(config)
            all_detected.extend(detected)

            # Call callback for each detected asset
            if self.on_asset_detected and detected:
                for asset in detected:
                    try:
                        await self._call_callback(self.on_asset_detected, asset)
                    except Exception as e:
                        logger.error(f"Callback error: {e}")

        self.stats["last_check"] = datetime.now().isoformat()
        return all_detected

    async def _call_callback(self, callback: Callable, *args):
        """Call a callback (sync or async)"""
        if asyncio.iscoroutinefunction(callback):
            await callback(*args)
        else:
            callback(*args)

    async def start(self):
        """Start the folder watcher service"""
        self.running = True
        self.stats["start_time"] = datetime.now().isoformat()
        logger.info(f"FolderWatcher started - monitoring {len(self.watch_configs)} folders")

        while self.running:
            try:
                detected = await self.scan_all_folders()

                if detected and self.on_asset_ready:
                    for asset in detected:
                        try:
                            await self._call_callback(self.on_asset_ready, asset)
                        except Exception as e:
                            logger.error(f"Asset ready callback error: {e}")
                            if self.on_error:
                                await self._call_callback(self.on_error, asset, e)

            except Exception as e:
                logger.error(f"Scan error: {e}")

            await asyncio.sleep(self.check_interval)

    def stop(self):
        """Stop the folder watcher service"""
        self.running = False
        self._save_state()
        logger.info("FolderWatcher stopped")

    def _save_state(self):
        """Save watcher state to file"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            state = {
                "watch_configs": {
                    path: {
                        "path": cfg.path,
                        "name": cfg.name,
                        "enabled": cfg.enabled,
                        "recursive": cfg.recursive,
                        "file_types": cfg.file_types,
                        "trigger_agents": cfg.trigger_agents,
                        "priority": cfg.priority
                    }
                    for path, cfg in self.watch_configs.items()
                },
                "processed_files": list(self.processed_files)[-1000:],  # Keep last 1000
                "stats": self.stats
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def _load_state(self):
        """Load watcher state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)

                # Restore processed files
                self.processed_files = set(state.get("processed_files", []))

                # Restore watch configs
                for path, cfg_data in state.get("watch_configs", {}).items():
                    self.watch_configs[path] = WatchConfig(**cfg_data)

                logger.info(f"Loaded state: {len(self.watch_configs)} watch folders")
        except Exception as e:
            logger.warning(f"Failed to load state: {e}")

    def get_stats(self) -> Dict:
        """Get watcher statistics"""
        return {
            **self.stats,
            "watch_folders": len(self.watch_configs),
            "pending_files": len(self.pending_files),
            "processed_count": len(self.processed_files),
            "running": self.running
        }


# Default watch folder configurations for MAM systems
DEFAULT_MAM_CONFIGS = {
    "avid_ingest": WatchConfig(
        path="/mnt/avid/ingest",
        name="Avid Ingest",
        file_types=["video", "audio"],
        trigger_agents=["caption", "clip", "compliance", "archive"],
        priority="high",
        metadata={"mam_system": "avid"}
    ),
    "grass_valley_hot": WatchConfig(
        path="/mnt/gv/hotfolder",
        name="Grass Valley Hot Folder",
        file_types=["video"],
        trigger_agents=["all"],
        priority="high",
        metadata={"mam_system": "grass_valley"}
    ),
    "social_export": WatchConfig(
        path="/mnt/social/export",
        name="Social Media Export",
        file_types=["video"],
        trigger_agents=["clip", "social", "trending"],
        priority="normal",
        metadata={"workflow": "social"}
    ),
    "compliance_review": WatchConfig(
        path="/mnt/compliance/review",
        name="Compliance Review",
        file_types=["video", "audio"],
        trigger_agents=["compliance", "caption"],
        priority="critical",
        metadata={"workflow": "compliance"}
    ),
    "archive_ingest": WatchConfig(
        path="/mnt/archive/ingest",
        name="Archive Ingest",
        file_types=["video", "audio", "image"],
        trigger_agents=["archive", "rights"],
        priority="normal",
        metadata={"workflow": "archive"}
    ),
}
