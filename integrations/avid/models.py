"""
Avid Media Central CTMS Data Models

Pydantic models for CTMS (Connectivity Toolkit Media Services) API responses.
Follows the HAL (Hypertext Application Language) JSON format used by Avid.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    """Avid asset types."""
    CLIP = "clip"
    SUBCLIP = "subclip"
    SEQUENCE = "sequence"
    BIN = "bin"
    FOLDER = "folder"
    GRAPHIC = "graphic"
    AUDIO = "audio"
    EFFECT = "effect"


class CTMSLink(BaseModel):
    """
    HAL link in CTMS response.

    CTMS uses HAL (Hypertext Application Language) for hypermedia.
    Links allow navigation between resources.
    """
    href: str
    title: Optional[str] = None
    type: Optional[str] = None
    templated: Optional[bool] = False

    class Config:
        extra = "allow"


class CTMSLinks(BaseModel):
    """Collection of HAL links."""
    self_link: Optional[CTMSLink] = Field(None, alias="self")
    parent: Optional[CTMSLink] = None
    children: Optional[CTMSLink] = None
    download: Optional[CTMSLink] = None
    thumbnail: Optional[CTMSLink] = None
    proxy: Optional[CTMSLink] = None
    edit: Optional[CTMSLink] = None

    class Config:
        extra = "allow"
        populate_by_name = True


class CTMSAsset(BaseModel):
    """
    Avid Media Central asset representation.

    Represents clips, sequences, bins, and other assets
    stored in Avid Interplay or MediaCentral.
    """
    id: str = Field(..., description="Unique asset identifier (mob ID)")
    name: str = Field(..., description="Asset display name")
    type: AssetType = Field(default=AssetType.CLIP, description="Asset type")

    # Timing information
    duration: Optional[int] = Field(None, description="Duration in frames")
    start_timecode: Optional[str] = Field(None, description="Start timecode")
    end_timecode: Optional[str] = Field(None, description="End timecode")
    frame_rate: Optional[float] = Field(None, description="Frame rate")

    # Dates
    created: Optional[datetime] = Field(None, description="Creation date")
    modified: Optional[datetime] = Field(None, description="Last modified date")

    # Location
    workspace: Optional[str] = Field(None, description="Workspace/project name")
    path: Optional[str] = Field(None, description="Path in Interplay")
    bin_path: Optional[str] = Field(None, description="Bin location")

    # Media info
    video_tracks: Optional[int] = Field(None, description="Number of video tracks")
    audio_tracks: Optional[int] = Field(None, description="Number of audio tracks")
    resolution: Optional[str] = Field(None, description="Video resolution")
    codec: Optional[str] = Field(None, description="Video codec")

    # Metadata
    description: Optional[str] = None
    keywords: Optional[List[str]] = Field(default_factory=list)
    custom_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    # HAL links
    links: Optional[CTMSLinks] = Field(None, alias="_links")

    class Config:
        extra = "allow"
        populate_by_name = True

    @property
    def duration_seconds(self) -> Optional[float]:
        """Get duration in seconds."""
        if self.duration and self.frame_rate:
            return self.duration / self.frame_rate
        return None

    @property
    def thumbnail_url(self) -> Optional[str]:
        """Get thumbnail URL if available."""
        if self.links and self.links.thumbnail:
            return self.links.thumbnail.href
        return None

    def to_generic_asset(self):
        """Convert to generic Asset model."""
        from ..base import Asset
        return Asset(
            id=self.id,
            name=self.name,
            asset_type=self.type.value,
            duration=self.duration,
            created_at=self.created,
            modified_at=self.modified,
            metadata={
                "workspace": self.workspace,
                "path": self.path,
                "resolution": self.resolution,
                "keywords": self.keywords
            },
            source_system="avid",
            thumbnail_url=self.thumbnail_url
        )


class CTMSSearchResult(BaseModel):
    """
    CTMS search result response.

    Contains paginated list of assets matching search criteria.
    """
    total_count: int = Field(0, alias="totalCount")
    page: int = Field(1, alias="page")
    page_size: int = Field(50, alias="pageSize")
    assets: List[CTMSAsset] = Field(default_factory=list, alias="items")

    # HAL embedded content
    embedded: Optional[Dict[str, Any]] = Field(None, alias="_embedded")
    links: Optional[CTMSLinks] = Field(None, alias="_links")

    class Config:
        extra = "allow"
        populate_by_name = True

    @classmethod
    def from_hal_response(cls, response: Dict[str, Any]) -> "CTMSSearchResult":
        """Parse HAL+JSON response into SearchResult."""
        embedded = response.get("_embedded", {})
        items = embedded.get("items", embedded.get("assets", []))

        return cls(
            total_count=response.get("totalCount", len(items)),
            page=response.get("page", 1),
            page_size=response.get("pageSize", 50),
            assets=[CTMSAsset(**item) for item in items],
            links=response.get("_links")
        )


class CTMSWorkspace(BaseModel):
    """
    Avid Interplay workspace/project.

    Represents a workspace in Interplay Production.
    """
    id: str
    name: str
    description: Optional[str] = None
    path: str
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    owner: Optional[str] = None

    # Access info
    read_access: bool = True
    write_access: bool = False

    links: Optional[CTMSLinks] = Field(None, alias="_links")

    class Config:
        extra = "allow"
        populate_by_name = True


class CTMSIngestJob(BaseModel):
    """
    CTMS ingest job status.

    Tracks the progress of an asset ingest operation.
    """
    job_id: str = Field(..., alias="jobId")
    status: str  # "pending", "processing", "completed", "failed"
    progress: int = Field(0, ge=0, le=100)
    asset_id: Optional[str] = Field(None, alias="assetId")
    error_message: Optional[str] = Field(None, alias="errorMessage")
    created: datetime
    completed: Optional[datetime] = None

    class Config:
        extra = "allow"
        populate_by_name = True


class CTMSRegistry(BaseModel):
    """
    CTMS Registry response.

    The registry is the entry point for CTMS API discovery.
    It provides links to all available services.
    """
    services: Dict[str, CTMSLink] = Field(default_factory=dict)
    version: Optional[str] = None

    @classmethod
    def from_hal_response(cls, response: Dict[str, Any]) -> "CTMSRegistry":
        """Parse registry HAL response."""
        links = response.get("_links", {})
        services = {}
        for key, value in links.items():
            if isinstance(value, dict):
                services[key] = CTMSLink(**value)
        return cls(
            services=services,
            version=response.get("version")
        )
