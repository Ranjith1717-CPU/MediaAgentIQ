"""
MediaAgentIQ Integrations Package

Provides connectors for broadcast industry systems:
- Avid Media Central (CTMS)
- Grass Valley GV Orbit (NMOS IS-04/IS-05)
- MOS Protocol (Newsroom systems)
- BXF (Schedule exchange)
"""

from .base import (
    BroadcastConnector,
    ConnectionStatus,
    IntegrationError,
    AuthenticationError,
    ConnectionError as BroadcastConnectionError
)

from .avid import AvidConnector, AvidMockConnector
from .grass_valley import NMOSClient

__all__ = [
    # Base classes
    "BroadcastConnector",
    "ConnectionStatus",
    "IntegrationError",
    "AuthenticationError",
    "BroadcastConnectionError",
    # Avid
    "AvidConnector",
    "AvidMockConnector",
    # Grass Valley
    "NMOSClient",
]
