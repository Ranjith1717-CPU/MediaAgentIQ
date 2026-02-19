"""
Avid Media Central CTMS Connector

Provides integration with Avid Media Central using the CTMS
(Connectivity Toolkit Media Services) REST API.

CTMS follows HATEOAS principles using HAL (Hypertext Application Language)
for hypermedia. All navigation is done through _links in responses.

Key endpoints:
- /apis - Registry (API discovery)
- /search - Asset search
- /assets/{id} - Asset details
- /workspaces - Available workspaces
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import httpx

from ..base import (
    BroadcastConnector,
    ConnectionStatus,
    Asset,
    SearchResult,
    AuthenticationError,
    ConnectionError as BroadcastConnectionError
)
from .models import CTMSAsset, CTMSSearchResult, CTMSRegistry, CTMSWorkspace
from .auth import AvidAuthManager, AvidMockAuth

logger = logging.getLogger(__name__)


class AvidConnector(BroadcastConnector):
    """
    Avid Media Central CTMS Connector.

    Connects to Avid Interplay Production and MediaCentral
    through the CTMS REST API.

    Usage:
        connector = AvidConnector(
            host="https://avid-server.example.com",
            username="user",
            password="pass",
            workspace="default"
        )
        await connector.connect()
        results = await connector.search_assets("breaking news")
        await connector.disconnect()
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        workspace: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize Avid connector.

        Args:
            host: Avid Media Central CTMS host URL
            username: Authentication username
            password: Authentication password
            workspace: Default workspace name
            timeout: Request timeout in seconds
        """
        super().__init__("Avid Media Central")
        self.host = host.rstrip("/")
        self.workspace = workspace
        self.timeout = timeout

        self._auth = AvidAuthManager(host, username, password)
        self._client: Optional[httpx.AsyncClient] = None
        self._registry: Optional[CTMSRegistry] = None

    async def connect(self) -> bool:
        """
        Connect to Avid Media Central.

        Performs:
        1. Authentication
        2. Registry discovery
        3. Connection validation

        Returns:
            True if connection successful
        """
        try:
            self._set_status(ConnectionStatus.CONNECTING)

            # Authenticate
            await self._auth.authenticate()

            # Create HTTP client
            self._client = httpx.AsyncClient(
                base_url=self.host,
                headers=self._auth.get_auth_headers(),
                timeout=self.timeout
            )

            # Discover API registry
            self._registry = await self._discover_registry()

            self._set_status(ConnectionStatus.AUTHENTICATED)
            logger.info(f"Connected to Avid Media Central at {self.host}")
            return True

        except AuthenticationError as e:
            self._set_error(f"Authentication failed: {e}")
            return False
        except Exception as e:
            self._set_error(f"Connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Avid."""
        if self._client:
            await self._client.aclose()
            self._client = None

        await self._auth.logout()
        self._set_status(ConnectionStatus.DISCONNECTED)
        logger.info("Disconnected from Avid Media Central")

    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection.

        Returns:
            Dict with connection test results
        """
        result = {
            "connected": False,
            "host": self.host,
            "authenticated": self._auth.is_authenticated,
            "registry_available": self._registry is not None,
            "error": None
        }

        try:
            if not self._client:
                await self.connect()

            # Test by fetching registry
            response = await self._client.get("/apis")
            result["connected"] = response.status_code == 200
            result["version"] = self._registry.version if self._registry else None

        except Exception as e:
            result["error"] = str(e)

        return result

    async def search_assets(
        self,
        query: str,
        filters: Dict[str, Any] = None,
        page: int = 1,
        page_size: int = 50
    ) -> SearchResult:
        """
        Search for assets in Avid.

        Args:
            query: Search query
            filters: Optional filters (type, date_from, date_to, workspace)
            page: Page number
            page_size: Results per page

        Returns:
            SearchResult with matching assets
        """
        await self._ensure_connected()

        # Build search parameters
        params = {
            "q": query,
            "page": page,
            "pageSize": page_size
        }

        if filters:
            if "type" in filters:
                params["type"] = filters["type"]
            if "workspace" in filters:
                params["workspace"] = filters["workspace"]
            elif self.workspace:
                params["workspace"] = self.workspace
            if "date_from" in filters:
                params["modifiedAfter"] = filters["date_from"]
            if "date_to" in filters:
                params["modifiedBefore"] = filters["date_to"]

        # Get search endpoint from registry
        search_url = self._get_service_url("search", "/search")

        logger.debug(f"Searching Avid: {query}")
        start_time = datetime.now()

        response = await self._client.get(search_url, params=params)
        response.raise_for_status()

        elapsed_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        # Parse HAL response
        ctms_result = CTMSSearchResult.from_hal_response(response.json())

        # Convert to generic SearchResult
        assets = [asset.to_generic_asset() for asset in ctms_result.assets]

        return SearchResult(
            total_count=ctms_result.total_count,
            page=ctms_result.page,
            page_size=ctms_result.page_size,
            assets=assets,
            query=query,
            search_time_ms=elapsed_ms
        )

    async def get_asset(self, asset_id: str) -> Optional[Asset]:
        """
        Get asset by ID.

        Args:
            asset_id: Avid mob ID

        Returns:
            Asset if found, None otherwise
        """
        await self._ensure_connected()

        try:
            response = await self._client.get(f"/assets/{asset_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()

            ctms_asset = CTMSAsset(**response.json())
            return ctms_asset.to_generic_asset()

        except httpx.HTTPStatusError:
            return None

    async def ingest_asset(
        self,
        file_path: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Ingest asset into Avid.

        Args:
            file_path: Path to file
            metadata: Asset metadata (name, description, etc.)

        Returns:
            Asset ID of ingested content
        """
        await self._ensure_connected()

        # Get ingest endpoint
        ingest_url = self._get_service_url("ingest", "/ingest")

        # Create ingest job
        job_data = {
            "name": metadata.get("name", "Untitled"),
            "description": metadata.get("description", ""),
            "workspace": metadata.get("workspace", self.workspace),
            "targetBin": metadata.get("bin", "/Incoming"),
            "sourceUri": file_path
        }

        response = await self._client.post(ingest_url, json=job_data)
        response.raise_for_status()

        job = response.json()
        return job.get("assetId", job.get("jobId"))

    async def get_workspaces(self) -> List[CTMSWorkspace]:
        """
        Get available workspaces.

        Returns:
            List of CTMSWorkspace
        """
        await self._ensure_connected()

        workspaces_url = self._get_service_url("workspaces", "/workspaces")
        response = await self._client.get(workspaces_url)
        response.raise_for_status()

        data = response.json()
        items = data.get("_embedded", {}).get("items", [])
        return [CTMSWorkspace(**ws) for ws in items]

    # ==================== Private Methods ====================

    async def _discover_registry(self) -> CTMSRegistry:
        """Discover CTMS API registry."""
        response = await self._client.get("/apis")
        response.raise_for_status()
        return CTMSRegistry.from_hal_response(response.json())

    async def _ensure_connected(self) -> None:
        """Ensure we're connected, reconnecting if needed."""
        if not self.is_connected:
            await self.connect()

        # Ensure token is valid
        await self._auth.ensure_valid_token()
        self._client.headers.update(self._auth.get_auth_headers())

    def _get_service_url(self, service: str, default: str) -> str:
        """Get service URL from registry."""
        if self._registry and service in self._registry.services:
            return self._registry.services[service].href
        return default


class AvidMockConnector(BroadcastConnector):
    """
    Mock Avid connector for development and testing.

    Returns realistic mock data without connecting to a real Avid system.
    Use this when AVID_MOCK_MODE=true.
    """

    def __init__(
        self,
        host: str = "mock://avid-server",
        username: str = "mock-user",
        password: str = "mock-pass",
        workspace: str = "MockWorkspace"
    ):
        super().__init__("Avid Media Central (Mock)")
        self.host = host
        self.workspace = workspace

    async def connect(self) -> bool:
        """Mock connection."""
        self._set_status(ConnectionStatus.MOCK)
        logger.info("Connected to Mock Avid (development mode)")
        return True

    async def disconnect(self) -> None:
        """Mock disconnect."""
        self._set_status(ConnectionStatus.DISCONNECTED)

    async def test_connection(self) -> Dict[str, Any]:
        """Return mock connection test."""
        return {
            "connected": True,
            "host": self.host,
            "authenticated": True,
            "registry_available": True,
            "mock_mode": True,
            "error": None
        }

    async def search_assets(
        self,
        query: str,
        filters: Dict[str, Any] = None,
        page: int = 1,
        page_size: int = 50
    ) -> SearchResult:
        """Return mock search results."""
        # Generate mock assets based on query
        mock_assets = self._generate_mock_assets(query, page_size)

        return SearchResult(
            total_count=len(mock_assets) * 3,  # Pretend there are more pages
            page=page,
            page_size=page_size,
            assets=mock_assets,
            query=query,
            search_time_ms=125
        )

    async def get_asset(self, asset_id: str) -> Optional[Asset]:
        """Return mock asset."""
        return Asset(
            id=asset_id,
            name=f"Asset {asset_id[:8]}",
            asset_type="clip",
            duration=1800,  # 1 minute at 30fps
            created_at=datetime.now(),
            metadata={
                "workspace": self.workspace,
                "resolution": "1920x1080",
                "codec": "DNxHD"
            },
            source_system="avid-mock"
        )

    async def ingest_asset(
        self,
        file_path: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Mock ingest, return fake asset ID."""
        import uuid
        return f"mock-{uuid.uuid4().hex[:12]}"

    def _generate_mock_assets(self, query: str, count: int = 10) -> List[Asset]:
        """Generate mock assets based on query."""
        templates = [
            ("Breaking News Coverage", "clip", 3600),
            ("Interview Segment", "clip", 1800),
            ("Sports Highlights", "sequence", 900),
            ("Weather Report", "clip", 300),
            ("Commercial Break", "sequence", 120),
            ("Live Event Recording", "clip", 7200),
            ("News Package", "sequence", 180),
            ("B-Roll Footage", "clip", 600),
        ]

        assets = []
        for i in range(min(count, len(templates) * 2)):
            template = templates[i % len(templates)]
            assets.append(Asset(
                id=f"avid-mock-{i:04d}",
                name=f"{template[0]} - {query}",
                asset_type=template[1],
                duration=template[2] * 30,  # Convert to frames
                created_at=datetime.now(),
                metadata={
                    "workspace": self.workspace,
                    "resolution": "1920x1080",
                    "keywords": [query, "news", "broadcast"]
                },
                source_system="avid-mock"
            ))

        return assets


def get_avid_connector(
    host: str,
    username: str,
    password: str,
    workspace: str = None,
    mock_mode: bool = False
) -> BroadcastConnector:
    """
    Factory function to get appropriate Avid connector.

    Args:
        host: Avid host URL
        username: Username
        password: Password
        workspace: Default workspace
        mock_mode: If True, return mock connector

    Returns:
        AvidConnector or AvidMockConnector
    """
    if mock_mode:
        return AvidMockConnector(host, username, password, workspace)
    return AvidConnector(host, username, password, workspace)
