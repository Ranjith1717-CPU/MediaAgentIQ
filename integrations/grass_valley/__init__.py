"""
Grass Valley Integration via NMOS

Provides IS-04 (Discovery & Registration) and IS-05 (Connection Management)
support for Grass Valley GV Orbit and other NMOS-compliant devices.

NMOS (Networked Media Open Specifications) is the control plane standard
for IP broadcast infrastructure (SMPTE ST 2110).

Features:
- Node/device discovery
- Sender/receiver enumeration
- Signal routing
- Health monitoring

Usage:
    from integrations.grass_valley import NMOSClient

    client = NMOSClient(registry_url="http://gv-orbit:8010")
    await client.connect()
    nodes = await client.get_nodes()
"""

from .nmos_client import NMOSClient, NMOSMockClient

__all__ = [
    "NMOSClient",
    "NMOSMockClient",
]
