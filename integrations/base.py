"""
Base classes for broadcast system integrations.

Defines the abstract interface that all broadcast connectors must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """Connection status for broadcast systems."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    ERROR = "error"
    MOCK = "mock"


class IntegrationError(Exception):
    """Base exception for integration errors."""
    pass


class AuthenticationError(IntegrationError):
    """Raised when authentication fails."""
    pass


class ConnectionError(IntegrationError):
    """Raised when connection fails."""
    pass


@dataclass
class Asset:
    """
    Generic media asset representation.

    Maps to assets from various systems (Avid, Grass Valley, etc.)
    """
    id: str
    name: str
    asset_type: str  # "clip", "sequence", "graphic", etc.
    duration: Optional[int] = None  # Duration in frames or milliseconds
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    source_system: str = "unknown"
    source_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.asset_type,
            "duration": self.duration,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "modified_at": self.modified_at.isoformat() if self.modified_at else None,
            "metadata": self.metadata or {},
            "source_system": self.source_system,
            "source_url": self.source_url,
            "thumbnail_url": self.thumbnail_url
        }


@dataclass
class SearchResult:
    """Search result from a broadcast system."""
    total_count: int
    page: int
    page_size: int
    assets: List[Asset]
    query: str
    search_time_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_count": self.total_count,
            "page": self.page,
            "page_size": self.page_size,
            "assets": [a.to_dict() for a in self.assets],
            "query": self.query,
            "search_time_ms": self.search_time_ms
        }


class BroadcastConnector(ABC):
    """
    Abstract base class for broadcast system integrations.

    All broadcast system connectors (Avid, Grass Valley, etc.)
    should inherit from this class and implement its methods.

    Usage:
        connector = AvidConnector(host, username, password)
        await connector.connect()
        results = await connector.search_assets("breaking news")
        await connector.disconnect()
    """

    def __init__(self, name: str):
        """
        Initialize the connector.

        Args:
            name: Human-readable name for this connector
        """
        self.name = name
        self._status = ConnectionStatus.DISCONNECTED
        self._connected_at: Optional[datetime] = None
        self._last_error: Optional[str] = None

    @property
    def status(self) -> ConnectionStatus:
        """Get current connection status."""
        return self._status

    @property
    def is_connected(self) -> bool:
        """Check if connected."""
        return self._status in (
            ConnectionStatus.CONNECTED,
            ConnectionStatus.AUTHENTICATED,
            ConnectionStatus.MOCK
        )

    @property
    def last_error(self) -> Optional[str]:
        """Get last error message."""
        return self._last_error

    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to the broadcast system.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the broadcast system."""
        pass

    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection and return status info.

        Returns:
            Dict with connection test results
        """
        pass

    @abstractmethod
    async def search_assets(
        self,
        query: str,
        filters: Dict[str, Any] = None,
        page: int = 1,
        page_size: int = 50
    ) -> SearchResult:
        """
        Search for media assets.

        Args:
            query: Search query string
            filters: Optional filter parameters
            page: Page number (1-indexed)
            page_size: Results per page

        Returns:
            SearchResult with matching assets
        """
        pass

    @abstractmethod
    async def get_asset(self, asset_id: str) -> Optional[Asset]:
        """
        Get a single asset by ID.

        Args:
            asset_id: Unique asset identifier

        Returns:
            Asset if found, None otherwise
        """
        pass

    @abstractmethod
    async def ingest_asset(
        self,
        file_path: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Ingest a new asset into the system.

        Args:
            file_path: Path to the file to ingest
            metadata: Asset metadata

        Returns:
            ID of the created asset
        """
        pass

    async def get_info(self) -> Dict[str, Any]:
        """
        Get connector information.

        Returns:
            Dict with connector status and info
        """
        return {
            "name": self.name,
            "status": self._status.value,
            "connected": self.is_connected,
            "connected_at": (
                self._connected_at.isoformat()
                if self._connected_at else None
            ),
            "last_error": self._last_error
        }

    def _set_status(self, status: ConnectionStatus) -> None:
        """Update connection status."""
        old_status = self._status
        self._status = status
        if status == ConnectionStatus.CONNECTED:
            self._connected_at = datetime.now()
        logger.debug(f"{self.name}: {old_status.value} -> {status.value}")

    def _set_error(self, error: str) -> None:
        """Record an error."""
        self._last_error = error
        self._status = ConnectionStatus.ERROR
        logger.error(f"{self.name}: {error}")
