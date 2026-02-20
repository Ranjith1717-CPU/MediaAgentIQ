"""
MediaAgentIQ Enterprise Integration Module

Provides autonomous background processing with MAM/PAM integration:
- Folder watching for new assets
- MAM system connectors (Avid, Grass Valley, etc.)
- Alert/notification services
- Automated agent orchestration
"""

# Core imports (no external dependencies)
from .folder_watcher import FolderWatcher, WatchConfig

__all__ = ['FolderWatcher', 'WatchConfig']

# Optional imports (require aiohttp)
try:
    from .notification_service import NotificationService, AlertLevel
    from .mam_connector import MAMConnector, AvidConnector, GrassValleyConnector
    from .autonomous_service import AutonomousService

    __all__.extend([
        'NotificationService', 'AlertLevel',
        'MAMConnector', 'AvidConnector', 'GrassValleyConnector',
        'AutonomousService'
    ])
    ENTERPRISE_AVAILABLE = True
except ImportError as e:
    ENTERPRISE_AVAILABLE = False
    import logging
    logging.getLogger(__name__).warning(
        f"Enterprise features require additional dependencies. Run: pip install aiohttp"
    )
