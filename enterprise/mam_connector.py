"""
MediaAgentIQ - MAM/PAM System Connectors

Integration connectors for Media Asset Management systems:
- Avid Media Central / Interplay
- Grass Valley GV STRATUS
- Generic REST/MOS connectors
- Custom webhook integrations
"""

import asyncio
import logging
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import aiohttp

logger = logging.getLogger("mam_connector")


class ConnectionStatus(Enum):
    """MAM connection status"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    AUTHENTICATED = "authenticated"


@dataclass
class MAMAsset:
    """Represents an asset in the MAM system"""
    id: str
    name: str
    path: str
    asset_type: str
    duration: Optional[float] = None
    size_bytes: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    status: str = "available"
    proxy_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "asset_type": self.asset_type,
            "duration": self.duration,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "modified_at": self.modified_at.isoformat() if self.modified_at else None,
            "metadata": self.metadata,
            "tags": self.tags,
            "status": self.status
        }


@dataclass
class MAMConfig:
    """Configuration for MAM connection"""
    name: str
    system_type: str  # avid, grass_valley, generic
    api_url: str
    username: str = ""
    password: str = ""
    api_key: str = ""
    workspace_id: str = ""
    timeout_seconds: int = 30
    verify_ssl: bool = True
    custom_headers: Dict = field(default_factory=dict)
    metadata_mapping: Dict = field(default_factory=dict)  # Map MediaAgentIQ fields to MAM fields


class MAMConnector(ABC):
    """
    Abstract base class for MAM system connectors.

    Provides common interface for all MAM integrations:
    - Authentication
    - Asset search and retrieval
    - Metadata read/write
    - Event notifications
    """

    def __init__(self, config: MAMConfig):
        self.config = config
        self.status = ConnectionStatus.DISCONNECTED
        self.session: Optional[aiohttp.ClientSession] = None
        self.auth_token: Optional[str] = None
        self.last_error: Optional[str] = None

        # Statistics
        self.stats = {
            "requests": 0,
            "successful": 0,
            "failed": 0,
            "last_request": None
        }

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to MAM system"""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from MAM system"""
        pass

    @abstractmethod
    async def search_assets(self, query: str, limit: int = 50) -> List[MAMAsset]:
        """Search for assets in MAM"""
        pass

    @abstractmethod
    async def get_asset(self, asset_id: str) -> Optional[MAMAsset]:
        """Get asset details by ID"""
        pass

    @abstractmethod
    async def update_metadata(self, asset_id: str, metadata: Dict) -> bool:
        """Update asset metadata in MAM"""
        pass

    @abstractmethod
    async def add_tags(self, asset_id: str, tags: List[str]) -> bool:
        """Add tags to an asset"""
        pass

    @abstractmethod
    async def notify_event(self, event_type: str, data: Dict) -> bool:
        """Send event notification to MAM"""
        pass

    async def _make_request(self, method: str, endpoint: str,
                           data: Optional[Dict] = None,
                           headers: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request to MAM API"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.config.api_url.rstrip('/')}/{endpoint.lstrip('/')}"

        request_headers = {
            "Content-Type": "application/json",
            **self.config.custom_headers
        }

        if self.auth_token:
            request_headers["Authorization"] = f"Bearer {self.auth_token}"

        if headers:
            request_headers.update(headers)

        self.stats["requests"] += 1
        self.stats["last_request"] = datetime.now().isoformat()

        try:
            async with self.session.request(
                method,
                url,
                json=data,
                headers=request_headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds),
                ssl=self.config.verify_ssl
            ) as response:
                if response.status in [200, 201, 202]:
                    self.stats["successful"] += 1
                    try:
                        return await response.json()
                    except:
                        return {"status": "success"}
                else:
                    self.stats["failed"] += 1
                    self.last_error = f"HTTP {response.status}"
                    logger.error(f"MAM request failed: {response.status}")
                    return None

        except asyncio.TimeoutError:
            self.stats["failed"] += 1
            self.last_error = "Request timeout"
            logger.error("MAM request timeout")
            return None

        except Exception as e:
            self.stats["failed"] += 1
            self.last_error = str(e)
            logger.error(f"MAM request error: {e}")
            return None

    def get_status(self) -> Dict:
        """Get connector status"""
        return {
            "name": self.config.name,
            "system_type": self.config.system_type,
            "status": self.status.value,
            "api_url": self.config.api_url,
            "authenticated": self.auth_token is not None,
            "last_error": self.last_error,
            "stats": self.stats
        }


class AvidConnector(MAMConnector):
    """
    Avid Media Central / Interplay MAM Connector

    Integrates with Avid's Media Asset Management platform:
    - Interplay Production
    - Media Central Cloud UX
    - Asset management API
    """

    async def connect(self) -> bool:
        """Connect and authenticate with Avid"""
        self.status = ConnectionStatus.CONNECTING

        try:
            # Avid authentication endpoint
            auth_data = {
                "username": self.config.username,
                "password": self.config.password
            }

            result = await self._make_request("POST", "/api/auth/login", auth_data)

            if result and "token" in result:
                self.auth_token = result["token"]
                self.status = ConnectionStatus.AUTHENTICATED
                logger.info(f"Connected to Avid: {self.config.name}")
                return True
            else:
                self.status = ConnectionStatus.ERROR
                return False

        except Exception as e:
            self.status = ConnectionStatus.ERROR
            self.last_error = str(e)
            logger.error(f"Avid connection failed: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Avid"""
        try:
            if self.auth_token:
                await self._make_request("POST", "/api/auth/logout")
            self.auth_token = None
            self.status = ConnectionStatus.DISCONNECTED
            if self.session:
                await self.session.close()
                self.session = None
            return True
        except:
            return False

    async def search_assets(self, query: str, limit: int = 50) -> List[MAMAsset]:
        """Search Avid for assets"""
        search_data = {
            "query": query,
            "limit": limit,
            "workspaceId": self.config.workspace_id
        }

        result = await self._make_request("POST", "/api/assets/search", search_data)

        if not result:
            return []

        assets = []
        for item in result.get("items", []):
            asset = MAMAsset(
                id=item.get("id", ""),
                name=item.get("name", ""),
                path=item.get("path", ""),
                asset_type=item.get("type", "unknown"),
                duration=item.get("duration"),
                size_bytes=item.get("size"),
                metadata=item.get("metadata", {}),
                tags=item.get("tags", []),
                proxy_url=item.get("proxyUrl"),
                thumbnail_url=item.get("thumbnailUrl")
            )
            assets.append(asset)

        return assets

    async def get_asset(self, asset_id: str) -> Optional[MAMAsset]:
        """Get Avid asset by ID"""
        result = await self._make_request("GET", f"/api/assets/{asset_id}")

        if not result:
            return None

        return MAMAsset(
            id=result.get("id", ""),
            name=result.get("name", ""),
            path=result.get("path", ""),
            asset_type=result.get("type", "unknown"),
            duration=result.get("duration"),
            size_bytes=result.get("size"),
            metadata=result.get("metadata", {}),
            tags=result.get("tags", [])
        )

    async def update_metadata(self, asset_id: str, metadata: Dict) -> bool:
        """Update Avid asset metadata"""
        # Map MediaAgentIQ metadata to Avid fields
        avid_metadata = {}
        for key, value in metadata.items():
            mapped_key = self.config.metadata_mapping.get(key, key)
            avid_metadata[mapped_key] = value

        result = await self._make_request(
            "PUT",
            f"/api/assets/{asset_id}/metadata",
            {"metadata": avid_metadata}
        )

        return result is not None

    async def add_tags(self, asset_id: str, tags: List[str]) -> bool:
        """Add tags to Avid asset"""
        result = await self._make_request(
            "POST",
            f"/api/assets/{asset_id}/tags",
            {"tags": tags}
        )
        return result is not None

    async def notify_event(self, event_type: str, data: Dict) -> bool:
        """Send event to Avid webhook"""
        event_data = {
            "eventType": event_type,
            "timestamp": datetime.now().isoformat(),
            "source": "MediaAgentIQ",
            "data": data
        }

        result = await self._make_request("POST", "/api/events", event_data)
        return result is not None

    async def create_marker(self, asset_id: str, timecode: str,
                           name: str, color: str = "blue") -> bool:
        """Create a marker on Avid timeline"""
        marker_data = {
            "assetId": asset_id,
            "timecode": timecode,
            "name": name,
            "color": color,
            "source": "MediaAgentIQ"
        }

        result = await self._make_request("POST", "/api/markers", marker_data)
        return result is not None


class GrassValleyConnector(MAMConnector):
    """
    Grass Valley GV STRATUS / EDIUS Connector

    Integrates with Grass Valley's media management:
    - GV STRATUS
    - EDIUS workflow
    - NMOS IS-04/IS-05
    """

    async def connect(self) -> bool:
        """Connect to Grass Valley system"""
        self.status = ConnectionStatus.CONNECTING

        try:
            # GV STRATUS API authentication
            auth_data = {
                "apiKey": self.config.api_key,
                "clientId": "MediaAgentIQ"
            }

            result = await self._make_request("POST", "/stratus/api/v1/auth", auth_data)

            if result and "sessionToken" in result:
                self.auth_token = result["sessionToken"]
                self.status = ConnectionStatus.AUTHENTICATED
                logger.info(f"Connected to Grass Valley: {self.config.name}")
                return True
            else:
                self.status = ConnectionStatus.ERROR
                return False

        except Exception as e:
            self.status = ConnectionStatus.ERROR
            self.last_error = str(e)
            logger.error(f"GV connection failed: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Grass Valley"""
        try:
            self.auth_token = None
            self.status = ConnectionStatus.DISCONNECTED
            if self.session:
                await self.session.close()
                self.session = None
            return True
        except:
            return False

    async def search_assets(self, query: str, limit: int = 50) -> List[MAMAsset]:
        """Search GV STRATUS for assets"""
        result = await self._make_request(
            "GET",
            f"/stratus/api/v1/assets?q={query}&limit={limit}"
        )

        if not result:
            return []

        assets = []
        for item in result.get("assets", []):
            asset = MAMAsset(
                id=item.get("assetId", ""),
                name=item.get("title", ""),
                path=item.get("location", ""),
                asset_type=item.get("mediaType", "unknown"),
                duration=item.get("durationMs", 0) / 1000,
                metadata=item.get("customFields", {}),
                tags=item.get("keywords", [])
            )
            assets.append(asset)

        return assets

    async def get_asset(self, asset_id: str) -> Optional[MAMAsset]:
        """Get GV asset by ID"""
        result = await self._make_request("GET", f"/stratus/api/v1/assets/{asset_id}")

        if not result:
            return None

        return MAMAsset(
            id=result.get("assetId", ""),
            name=result.get("title", ""),
            path=result.get("location", ""),
            asset_type=result.get("mediaType", "unknown"),
            duration=result.get("durationMs", 0) / 1000,
            metadata=result.get("customFields", {}),
            tags=result.get("keywords", [])
        )

    async def update_metadata(self, asset_id: str, metadata: Dict) -> bool:
        """Update GV asset metadata"""
        result = await self._make_request(
            "PATCH",
            f"/stratus/api/v1/assets/{asset_id}",
            {"customFields": metadata}
        )
        return result is not None

    async def add_tags(self, asset_id: str, tags: List[str]) -> bool:
        """Add keywords to GV asset"""
        result = await self._make_request(
            "POST",
            f"/stratus/api/v1/assets/{asset_id}/keywords",
            {"keywords": tags}
        )
        return result is not None

    async def notify_event(self, event_type: str, data: Dict) -> bool:
        """Send event to GV system"""
        result = await self._make_request(
            "POST",
            "/stratus/api/v1/events",
            {
                "type": event_type,
                "source": "MediaAgentIQ",
                "payload": data
            }
        )
        return result is not None


class GenericMAMConnector(MAMConnector):
    """
    Generic REST API MAM Connector

    Works with any MAM system that has a REST API.
    Configure endpoints via metadata_mapping.
    """

    def __init__(self, config: MAMConfig):
        super().__init__(config)
        self.endpoints = config.metadata_mapping.get("endpoints", {
            "auth": "/api/auth",
            "search": "/api/assets/search",
            "get": "/api/assets/{id}",
            "update": "/api/assets/{id}",
            "tags": "/api/assets/{id}/tags",
            "events": "/api/events"
        })

    async def connect(self) -> bool:
        """Generic authentication"""
        self.status = ConnectionStatus.CONNECTING

        try:
            auth_data = {}
            if self.config.username:
                auth_data["username"] = self.config.username
                auth_data["password"] = self.config.password
            if self.config.api_key:
                auth_data["apiKey"] = self.config.api_key

            result = await self._make_request("POST", self.endpoints["auth"], auth_data)

            if result:
                self.auth_token = result.get("token") or result.get("access_token") or result.get("sessionToken")
                if self.auth_token:
                    self.status = ConnectionStatus.AUTHENTICATED
                    return True

            self.status = ConnectionStatus.ERROR
            return False

        except Exception as e:
            self.status = ConnectionStatus.ERROR
            self.last_error = str(e)
            return False

    async def disconnect(self) -> bool:
        self.auth_token = None
        self.status = ConnectionStatus.DISCONNECTED
        if self.session:
            await self.session.close()
            self.session = None
        return True

    async def search_assets(self, query: str, limit: int = 50) -> List[MAMAsset]:
        result = await self._make_request(
            "POST",
            self.endpoints["search"],
            {"query": query, "limit": limit}
        )

        if not result:
            return []

        # Generic parsing - adapt based on response structure
        items = result.get("items") or result.get("assets") or result.get("data") or []
        assets = []

        for item in items:
            asset = MAMAsset(
                id=item.get("id") or item.get("assetId") or "",
                name=item.get("name") or item.get("title") or "",
                path=item.get("path") or item.get("location") or "",
                asset_type=item.get("type") or item.get("mediaType") or "unknown",
                metadata=item
            )
            assets.append(asset)

        return assets

    async def get_asset(self, asset_id: str) -> Optional[MAMAsset]:
        endpoint = self.endpoints["get"].replace("{id}", asset_id)
        result = await self._make_request("GET", endpoint)

        if not result:
            return None

        return MAMAsset(
            id=result.get("id") or asset_id,
            name=result.get("name") or result.get("title") or "",
            path=result.get("path") or "",
            asset_type=result.get("type") or "unknown",
            metadata=result
        )

    async def update_metadata(self, asset_id: str, metadata: Dict) -> bool:
        endpoint = self.endpoints["update"].replace("{id}", asset_id)
        result = await self._make_request("PATCH", endpoint, {"metadata": metadata})
        return result is not None

    async def add_tags(self, asset_id: str, tags: List[str]) -> bool:
        endpoint = self.endpoints["tags"].replace("{id}", asset_id)
        result = await self._make_request("POST", endpoint, {"tags": tags})
        return result is not None

    async def notify_event(self, event_type: str, data: Dict) -> bool:
        result = await self._make_request(
            "POST",
            self.endpoints["events"],
            {"type": event_type, "data": data}
        )
        return result is not None


def create_connector(config: MAMConfig) -> MAMConnector:
    """Factory function to create appropriate MAM connector"""
    connectors = {
        "avid": AvidConnector,
        "grass_valley": GrassValleyConnector,
        "generic": GenericMAMConnector
    }

    connector_class = connectors.get(config.system_type, GenericMAMConnector)
    return connector_class(config)
