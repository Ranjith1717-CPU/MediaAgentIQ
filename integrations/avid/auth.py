"""
Avid Media Central Authentication Manager

Handles token-based authentication with Avid CTMS.
Supports token refresh and session management.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import httpx

logger = logging.getLogger(__name__)


@dataclass
class AvidToken:
    """
    Avid authentication token.

    Contains access token and expiration information.
    """
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600  # Default 1 hour
    refresh_token: Optional[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def expires_at(self) -> datetime:
        """Get token expiration time."""
        return self.created_at + timedelta(seconds=self.expires_in)

    @property
    def is_expired(self) -> bool:
        """Check if token has expired."""
        # Consider expired 5 minutes before actual expiration
        buffer = timedelta(minutes=5)
        return datetime.now() >= (self.expires_at - buffer)

    @property
    def authorization_header(self) -> str:
        """Get Authorization header value."""
        return f"{self.token_type} {self.access_token}"


class AvidAuthManager:
    """
    Manages authentication with Avid Media Central.

    Handles:
    - Initial authentication
    - Token refresh
    - Session management

    Usage:
        auth = AvidAuthManager(host, username, password)
        token = await auth.authenticate()
        headers = auth.get_auth_headers()
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        auth_endpoint: str = "/auth/identity/connect/token"
    ):
        """
        Initialize auth manager.

        Args:
            host: Avid Media Central host URL
            username: Login username
            password: Login password
            auth_endpoint: OAuth token endpoint path
        """
        self.host = host.rstrip("/")
        self.username = username
        self.password = password
        self.auth_endpoint = auth_endpoint
        self._token: Optional[AvidToken] = None
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def is_authenticated(self) -> bool:
        """Check if we have a valid token."""
        return self._token is not None and not self._token.is_expired

    @property
    def token(self) -> Optional[AvidToken]:
        """Get current token."""
        return self._token

    async def authenticate(self) -> AvidToken:
        """
        Authenticate with Avid and get access token.

        Returns:
            AvidToken with access credentials

        Raises:
            AuthenticationError: If authentication fails
        """
        from ..base import AuthenticationError

        logger.info(f"Authenticating with Avid at {self.host}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.host}{self.auth_endpoint}",
                    data={
                        "grant_type": "password",
                        "username": self.username,
                        "password": self.password,
                        "client_id": "ctms-client",
                        "scope": "openid profile"
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    timeout=30.0
                )

                if response.status_code != 200:
                    error_msg = f"Authentication failed: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("error_description", error_msg)
                    except Exception:
                        pass
                    raise AuthenticationError(error_msg)

                data = response.json()
                self._token = AvidToken(
                    access_token=data["access_token"],
                    token_type=data.get("token_type", "Bearer"),
                    expires_in=data.get("expires_in", 3600),
                    refresh_token=data.get("refresh_token")
                )

                logger.info("Successfully authenticated with Avid")
                return self._token

        except httpx.RequestError as e:
            raise AuthenticationError(f"Connection error: {e}")

    async def refresh(self) -> AvidToken:
        """
        Refresh the access token.

        Returns:
            New AvidToken

        Raises:
            AuthenticationError: If refresh fails
        """
        from ..base import AuthenticationError

        if not self._token or not self._token.refresh_token:
            # No refresh token, do full authentication
            return await self.authenticate()

        logger.info("Refreshing Avid token")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.host}{self.auth_endpoint}",
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": self._token.refresh_token,
                        "client_id": "ctms-client"
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    timeout=30.0
                )

                if response.status_code != 200:
                    # Refresh failed, try full authentication
                    logger.warning("Token refresh failed, re-authenticating")
                    return await self.authenticate()

                data = response.json()
                self._token = AvidToken(
                    access_token=data["access_token"],
                    token_type=data.get("token_type", "Bearer"),
                    expires_in=data.get("expires_in", 3600),
                    refresh_token=data.get("refresh_token", self._token.refresh_token)
                )

                logger.info("Successfully refreshed Avid token")
                return self._token

        except httpx.RequestError:
            # Connection error during refresh, try full auth
            return await self.authenticate()

    async def ensure_valid_token(self) -> AvidToken:
        """
        Ensure we have a valid token, refreshing if needed.

        Returns:
            Valid AvidToken
        """
        if not self._token:
            return await self.authenticate()

        if self._token.is_expired:
            return await self.refresh()

        return self._token

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get headers for authenticated requests.

        Returns:
            Dict with Authorization and Accept headers
        """
        headers = {
            "Accept": "application/hal+json",
            "Content-Type": "application/json"
        }

        if self._token:
            headers["Authorization"] = self._token.authorization_header

        return headers

    async def logout(self) -> None:
        """Clear authentication token."""
        self._token = None
        logger.info("Logged out from Avid")


class AvidMockAuth(AvidAuthManager):
    """
    Mock authentication for development/testing.

    Returns fake tokens without making real API calls.
    """

    async def authenticate(self) -> AvidToken:
        """Return mock token."""
        logger.info("Mock authentication (no real Avid connection)")
        self._token = AvidToken(
            access_token="mock-token-for-development",
            token_type="Bearer",
            expires_in=86400  # 24 hours
        )
        return self._token

    async def refresh(self) -> AvidToken:
        """Return mock token."""
        return await self.authenticate()
