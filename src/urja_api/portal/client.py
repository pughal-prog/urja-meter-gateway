"""Asynchronous HTTP client for interacting with the legacy Urja Meter Ops portal.

Features:
- Session reuse and automated re-authentication on expiry
- Bounded retries with exponential backoff on 5xx / timeouts
- Polite client-side rate limiting (token bucket / leaky bucket)
- Strict Anti-Corruption boundaries
"""

import asyncio
import logging
from typing import Any

import httpx

from urja_api.config import Settings
from urja_api.portal.auth import PortalAuthManager

logger = logging.getLogger(__name__)


class PortalClient:
    """Anti-Corruption HTTP client interfacing with the legacy portal."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.auth_manager = PortalAuthManager(
            username=settings.portal_username,
            password=settings.portal_password,
            base_url=settings.portal_base_url,
        )
        self._client: httpx.AsyncClient | None = None
        self._rate_limiter_lock = asyncio.Lock()
        self._last_request_time = 0.0

    async def get_client(self) -> httpx.AsyncClient:
        """Provide or initialize shared httpx.AsyncClient."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.settings.portal_base_url,
                timeout=self.settings.portal_timeout_seconds,
            )
        return self._client

    async def close(self) -> None:
        """Close underlying HTTP client connections."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def execute_request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Execute request with rate-limiting, re-auth on 401, and retries.

        To be implemented in Phase 3 strictly per PROTOCOL.md.
        """
        raise NotImplementedError("Portal client request pipeline will be implemented in Phase 3.")
