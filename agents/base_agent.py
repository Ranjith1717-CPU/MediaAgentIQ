"""
Base Agent Class for MediaAgentIQ
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import json


class BaseAgent(ABC):
    """Base class for all MediaAgentIQ agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.created_at = datetime.now()

    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input and return results."""
        pass

    @abstractmethod
    async def validate_input(self, input_data: Any) -> bool:
        """Validate input data before processing."""
        pass

    def get_info(self) -> Dict[str, str]:
        """Get agent information."""
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }

    def format_timestamp(self, seconds: float) -> str:
        """Format seconds to SRT timestamp format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def format_vtt_timestamp(self, seconds: float) -> str:
        """Format seconds to VTT timestamp format (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def create_response(self, success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """Create a standardized response."""
        return {
            "success": success,
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "error": error
        }
