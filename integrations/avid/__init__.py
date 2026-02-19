"""
Avid Media Central Integration

Provides CTMS (Connectivity Toolkit Media Services) integration
for Avid Interplay Production, MediaCentral Asset Management,
and related Avid systems.

Features:
- Token-based authentication
- HAL+JSON response parsing
- Asset search and retrieval
- Clip ingest workflow
- Archive access

Usage:
    from integrations.avid import AvidConnector

    connector = AvidConnector(
        host="https://avid-server.example.com",
        username="user",
        password="pass"
    )
    await connector.connect()
    results = await connector.search_assets("breaking news")
"""

from .connector import AvidConnector, AvidMockConnector
from .models import CTMSAsset, CTMSSearchResult, CTMSWorkspace
from .auth import AvidAuthManager

__all__ = [
    "AvidConnector",
    "AvidMockConnector",
    "CTMSAsset",
    "CTMSSearchResult",
    "CTMSWorkspace",
    "AvidAuthManager",
]
