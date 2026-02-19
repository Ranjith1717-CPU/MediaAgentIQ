"""
Base Agent Class for MediaAgentIQ

Provides dual-path processing:
- Demo mode: Returns mock data for demonstration
- Production mode: Uses real AI services and integrations

All agents inherit from BaseAgent and implement:
- _demo_process(): Mock data processing
- _production_process(): Real AI/integration processing
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING
from datetime import datetime
import json
import logging

if TYPE_CHECKING:
    from settings import Settings

# Configure logging
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all MediaAgentIQ agents.

    Supports dual-mode processing:
    - Demo Mode (PRODUCTION_MODE=False): Uses mock data
    - Production Mode (PRODUCTION_MODE=True): Uses real APIs

    Args:
        name: Agent display name
        description: Agent description
        settings: Optional Settings instance (defaults to global settings)
    """

    def __init__(
        self,
        name: str,
        description: str,
        settings: Optional["Settings"] = None
    ):
        self.name = name
        self.description = description
        self.created_at = datetime.now()

        # Import settings here to avoid circular imports
        if settings is None:
            from settings import settings as default_settings
            self._settings = default_settings
        else:
            self._settings = settings

        logger.info(
            f"Initialized {self.name} | "
            f"Mode: {'Production' if self.is_production_mode else 'Demo'}"
        )

    @property
    def settings(self) -> "Settings":
        """Get the settings instance."""
        return self._settings

    @property
    def is_production_mode(self) -> bool:
        """Check if running in production mode."""
        return self._settings.PRODUCTION_MODE

    @property
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode."""
        return not self._settings.PRODUCTION_MODE

    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input and return results.

        Routes to demo or production processing based on settings.
        Validates input before processing.

        Args:
            input_data: Agent-specific input data

        Returns:
            Standardized response dict with success, data, error keys
        """
        # Validate input
        if not await self.validate_input(input_data):
            return self.create_response(
                success=False,
                error=f"Invalid input for {self.name}"
            )

        try:
            # Route to appropriate processing method
            if self.is_production_mode:
                logger.debug(f"{self.name}: Production processing")
                return await self._production_process(input_data)
            else:
                logger.debug(f"{self.name}: Demo processing")
                return await self._demo_process(input_data)

        except Exception as e:
            logger.error(f"{self.name} processing error: {e}", exc_info=True)
            return self.create_response(
                success=False,
                error=str(e)
            )

    @abstractmethod
    async def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data before processing.

        Args:
            input_data: Data to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    @abstractmethod
    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input in demo mode using mock data.

        This method should return realistic-looking mock data
        for demonstration purposes.

        Args:
            input_data: Agent-specific input

        Returns:
            Standardized response with mock data
        """
        pass

    @abstractmethod
    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input in production mode using real services.

        This method should use real AI APIs and integrations
        (OpenAI, Avid, etc.)

        Args:
            input_data: Agent-specific input

        Returns:
            Standardized response with real processed data
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Dict with agent metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__,
            "mode": "production" if self.is_production_mode else "demo",
            "created_at": self.created_at.isoformat()
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get agent status including integration readiness.

        Returns:
            Dict with status information
        """
        return {
            "name": self.name,
            "mode": "production" if self.is_production_mode else "demo",
            "ready": True,  # Override in subclasses for specific checks
            "integrations": self._get_required_integrations()
        }

    def _get_required_integrations(self) -> Dict[str, bool]:
        """
        Get status of integrations required by this agent.

        Override in subclasses to specify required integrations.

        Returns:
            Dict mapping integration name to configured status
        """
        return {}

    # ==================== Utility Methods ====================

    def format_timestamp(self, seconds: float) -> str:
        """
        Format seconds to SRT timestamp format (HH:MM:SS,mmm).

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def format_vtt_timestamp(self, seconds: float) -> str:
        """
        Format seconds to VTT timestamp format (HH:MM:SS.mmm).

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def create_response(
        self,
        success: bool,
        data: Any = None,
        error: str = None,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """
        Create a standardized response.

        Args:
            success: Whether processing succeeded
            data: Response data (agent-specific)
            error: Error message if failed
            metadata: Additional metadata

        Returns:
            Standardized response dict
        """
        response = {
            "success": success,
            "agent": self.name,
            "mode": "production" if self.is_production_mode else "demo",
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "error": error
        }

        if metadata:
            response["metadata"] = metadata

        return response

    def log_activity(self, action: str, details: str = None) -> None:
        """
        Log agent activity for tracking.

        Args:
            action: Action being performed
            details: Additional details
        """
        logger.info(
            f"{self.name} | {action}"
            + (f" | {details}" if details else "")
        )


class ProductionNotReadyError(Exception):
    """
    Raised when production processing is attempted
    but required services are not configured.
    """

    def __init__(self, agent_name: str, missing_config: str):
        self.agent_name = agent_name
        self.missing_config = missing_config
        super().__init__(
            f"{agent_name} requires {missing_config} for production mode"
        )
