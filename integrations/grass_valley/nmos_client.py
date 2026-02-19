"""
NMOS IS-04/IS-05 Client for Grass Valley Integration

Implements AMWA NMOS specifications for:
- IS-04: Discovery and Registration
- IS-05: Device Connection Management

Used with Grass Valley GV Orbit and other NMOS-compliant systems.

Key Concepts:
- Nodes: Physical/virtual devices running NMOS
- Devices: Logical groupings within nodes
- Sources: Origin points for media (cameras, graphics)
- Flows: Specific media streams
- Senders: Endpoints that transmit media
- Receivers: Endpoints that receive media
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import httpx
import uuid

logger = logging.getLogger(__name__)


class NMOSVersion(str, Enum):
    """NMOS API versions."""
    V1_0 = "v1.0"
    V1_1 = "v1.1"
    V1_2 = "v1.2"
    V1_3 = "v1.3"


@dataclass
class NMOSNode:
    """NMOS Node representation."""
    id: str
    label: str
    description: str = ""
    hostname: str = ""
    href: str = ""
    caps: Dict[str, Any] = field(default_factory=dict)
    services: List[Dict] = field(default_factory=list)
    clocks: List[Dict] = field(default_factory=list)
    interfaces: List[Dict] = field(default_factory=list)
    version: str = ""

    @classmethod
    def from_dict(cls, data: Dict) -> "NMOSNode":
        return cls(
            id=data.get("id", ""),
            label=data.get("label", ""),
            description=data.get("description", ""),
            hostname=data.get("hostname", ""),
            href=data.get("href", ""),
            caps=data.get("caps", {}),
            services=data.get("services", []),
            clocks=data.get("clocks", []),
            interfaces=data.get("interfaces", []),
            version=data.get("version", "")
        )


@dataclass
class NMOSDevice:
    """NMOS Device representation."""
    id: str
    label: str
    description: str = ""
    node_id: str = ""
    type: str = "urn:x-nmos:device:generic"
    senders: List[str] = field(default_factory=list)
    receivers: List[str] = field(default_factory=list)
    controls: List[Dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> "NMOSDevice":
        return cls(
            id=data.get("id", ""),
            label=data.get("label", ""),
            description=data.get("description", ""),
            node_id=data.get("node_id", ""),
            type=data.get("type", ""),
            senders=data.get("senders", []),
            receivers=data.get("receivers", []),
            controls=data.get("controls", [])
        )


@dataclass
class NMOSSender:
    """NMOS Sender (media source) representation."""
    id: str
    label: str
    description: str = ""
    flow_id: str = ""
    device_id: str = ""
    transport: str = "urn:x-nmos:transport:rtp"
    manifest_href: str = ""
    interface_bindings: List[str] = field(default_factory=list)
    subscription: Dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "NMOSSender":
        return cls(
            id=data.get("id", ""),
            label=data.get("label", ""),
            description=data.get("description", ""),
            flow_id=data.get("flow_id", ""),
            device_id=data.get("device_id", ""),
            transport=data.get("transport", ""),
            manifest_href=data.get("manifest_href", ""),
            interface_bindings=data.get("interface_bindings", []),
            subscription=data.get("subscription", {})
        )


@dataclass
class NMOSReceiver:
    """NMOS Receiver (media destination) representation."""
    id: str
    label: str
    description: str = ""
    device_id: str = ""
    transport: str = "urn:x-nmos:transport:rtp"
    format: str = "urn:x-nmos:format:video"
    caps: Dict = field(default_factory=dict)
    subscription: Dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "NMOSReceiver":
        return cls(
            id=data.get("id", ""),
            label=data.get("label", ""),
            description=data.get("description", ""),
            device_id=data.get("device_id", ""),
            transport=data.get("transport", ""),
            format=data.get("format", ""),
            caps=data.get("caps", {}),
            subscription=data.get("subscription", {})
        )


class NMOSClient:
    """
    NMOS IS-04/IS-05 Client.

    Connects to NMOS Registry (IS-04) for discovery and
    individual nodes (IS-05) for connection management.

    Usage:
        client = NMOSClient("http://registry:8010")
        await client.connect()
        nodes = await client.get_nodes()
        senders = await client.get_senders()

        # Route a signal
        await client.connect_sender_to_receiver(sender_id, receiver_id)
    """

    def __init__(
        self,
        registry_url: str,
        version: NMOSVersion = NMOSVersion.V1_3,
        timeout: int = 10
    ):
        """
        Initialize NMOS client.

        Args:
            registry_url: NMOS Registry URL (IS-04 Query API)
            version: NMOS API version
            timeout: Request timeout in seconds
        """
        self.registry_url = registry_url.rstrip("/")
        self.version = version
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._connected = False

    @property
    def query_api_url(self) -> str:
        """Get IS-04 Query API URL."""
        return f"{self.registry_url}/x-nmos/query/{self.version.value}"

    @property
    def is_connected(self) -> bool:
        """Check if connected."""
        return self._connected

    async def connect(self) -> bool:
        """
        Connect to NMOS Registry.

        Returns:
            True if connection successful
        """
        try:
            self._client = httpx.AsyncClient(timeout=self.timeout)

            # Test connection by querying root
            response = await self._client.get(f"{self.query_api_url}/")
            if response.status_code == 200:
                self._connected = True
                logger.info(f"Connected to NMOS Registry at {self.registry_url}")
                return True

            logger.warning(f"NMOS Registry returned {response.status_code}")
            return False

        except Exception as e:
            logger.error(f"Failed to connect to NMOS Registry: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from NMOS Registry."""
        if self._client:
            await self._client.aclose()
            self._client = None
        self._connected = False
        logger.info("Disconnected from NMOS Registry")

    async def get_nodes(self) -> List[NMOSNode]:
        """
        Get all registered nodes.

        Returns:
            List of NMOSNode
        """
        response = await self._client.get(f"{self.query_api_url}/nodes")
        response.raise_for_status()
        return [NMOSNode.from_dict(n) for n in response.json()]

    async def get_node(self, node_id: str) -> Optional[NMOSNode]:
        """Get a specific node by ID."""
        response = await self._client.get(f"{self.query_api_url}/nodes/{node_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return NMOSNode.from_dict(response.json())

    async def get_devices(self, node_id: str = None) -> List[NMOSDevice]:
        """
        Get registered devices.

        Args:
            node_id: Optional filter by node

        Returns:
            List of NMOSDevice
        """
        url = f"{self.query_api_url}/devices"
        params = {"node_id": node_id} if node_id else {}
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return [NMOSDevice.from_dict(d) for d in response.json()]

    async def get_senders(self, device_id: str = None) -> List[NMOSSender]:
        """
        Get registered senders.

        Args:
            device_id: Optional filter by device

        Returns:
            List of NMOSSender
        """
        url = f"{self.query_api_url}/senders"
        params = {"device_id": device_id} if device_id else {}
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return [NMOSSender.from_dict(s) for s in response.json()]

    async def get_receivers(self, device_id: str = None) -> List[NMOSReceiver]:
        """
        Get registered receivers.

        Args:
            device_id: Optional filter by device

        Returns:
            List of NMOSReceiver
        """
        url = f"{self.query_api_url}/receivers"
        params = {"device_id": device_id} if device_id else {}
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return [NMOSReceiver.from_dict(r) for r in response.json()]

    async def connect_sender_to_receiver(
        self,
        sender_id: str,
        receiver_id: str,
        receiver_node_url: str
    ) -> bool:
        """
        Create connection from sender to receiver (IS-05).

        Args:
            sender_id: Source sender ID
            receiver_id: Target receiver ID
            receiver_node_url: Node URL hosting the receiver

        Returns:
            True if connection successful
        """
        connection_url = (
            f"{receiver_node_url}/x-nmos/connection/v1.1"
            f"/single/receivers/{receiver_id}/staged"
        )

        payload = {
            "sender_id": sender_id,
            "master_enable": True,
            "activation": {
                "mode": "activate_immediate"
            }
        }

        response = await self._client.patch(connection_url, json=payload)
        return response.status_code in (200, 202)

    async def disconnect_receiver(
        self,
        receiver_id: str,
        receiver_node_url: str
    ) -> bool:
        """
        Disconnect a receiver (IS-05).

        Args:
            receiver_id: Receiver to disconnect
            receiver_node_url: Node URL hosting the receiver

        Returns:
            True if disconnection successful
        """
        connection_url = (
            f"{receiver_node_url}/x-nmos/connection/v1.1"
            f"/single/receivers/{receiver_id}/staged"
        )

        payload = {
            "sender_id": None,
            "master_enable": False,
            "activation": {
                "mode": "activate_immediate"
            }
        }

        response = await self._client.patch(connection_url, json=payload)
        return response.status_code in (200, 202)

    async def get_connection_status(
        self,
        receiver_id: str,
        receiver_node_url: str
    ) -> Dict[str, Any]:
        """
        Get receiver connection status (IS-05).

        Args:
            receiver_id: Receiver ID
            receiver_node_url: Node URL

        Returns:
            Connection status dict
        """
        connection_url = (
            f"{receiver_node_url}/x-nmos/connection/v1.1"
            f"/single/receivers/{receiver_id}/active"
        )

        response = await self._client.get(connection_url)
        response.raise_for_status()
        return response.json()


class NMOSMockClient:
    """
    Mock NMOS client for development.

    Returns realistic mock data without real NMOS connection.
    """

    def __init__(
        self,
        registry_url: str = "mock://nmos-registry",
        version: NMOSVersion = NMOSVersion.V1_3,
        timeout: int = 10
    ):
        self.registry_url = registry_url
        self.version = version
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def connect(self) -> bool:
        self._connected = True
        logger.info("Connected to Mock NMOS Registry")
        return True

    async def disconnect(self) -> None:
        self._connected = False

    async def get_nodes(self) -> List[NMOSNode]:
        """Return mock nodes."""
        return [
            NMOSNode(
                id=str(uuid.uuid4()),
                label="GV Orbit Main",
                description="Grass Valley GV Orbit Controller",
                hostname="gv-orbit-main"
            ),
            NMOSNode(
                id=str(uuid.uuid4()),
                label="Camera 1",
                description="LDX 100 4K Camera",
                hostname="cam-1"
            ),
            NMOSNode(
                id=str(uuid.uuid4()),
                label="Router Core",
                description="GV Ultrix IP Router",
                hostname="router-core"
            )
        ]

    async def get_devices(self, node_id: str = None) -> List[NMOSDevice]:
        """Return mock devices."""
        return [
            NMOSDevice(
                id=str(uuid.uuid4()),
                label="Camera 1 - Main",
                description="Primary camera device",
                type="urn:x-nmos:device:generic"
            )
        ]

    async def get_senders(self, device_id: str = None) -> List[NMOSSender]:
        """Return mock senders."""
        return [
            NMOSSender(
                id=str(uuid.uuid4()),
                label="Cam1-Video",
                description="Camera 1 Video Output",
                transport="urn:x-nmos:transport:rtp"
            ),
            NMOSSender(
                id=str(uuid.uuid4()),
                label="Cam1-Audio",
                description="Camera 1 Audio Output",
                transport="urn:x-nmos:transport:rtp"
            )
        ]

    async def get_receivers(self, device_id: str = None) -> List[NMOSReceiver]:
        """Return mock receivers."""
        return [
            NMOSReceiver(
                id=str(uuid.uuid4()),
                label="ME1-Input1",
                description="Multiviewer Input 1",
                format="urn:x-nmos:format:video"
            ),
            NMOSReceiver(
                id=str(uuid.uuid4()),
                label="Record1-In",
                description="Recorder Input",
                format="urn:x-nmos:format:video"
            )
        ]

    async def connect_sender_to_receiver(
        self,
        sender_id: str,
        receiver_id: str,
        receiver_node_url: str
    ) -> bool:
        logger.info(f"Mock: Connected {sender_id} -> {receiver_id}")
        return True

    async def disconnect_receiver(
        self,
        receiver_id: str,
        receiver_node_url: str
    ) -> bool:
        logger.info(f"Mock: Disconnected {receiver_id}")
        return True
