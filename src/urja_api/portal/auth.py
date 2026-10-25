"""Authentication and session handling for the legacy Urja Meter Ops portal.

Manages credentials exchange, CSRF extraction, cookie storage, and session validation.
Strictly implemented according to PROTOCOL.md once facts are discovered.
"""

import httpx


class PortalAuthManager:
    """Manages authentication tokens, cookies, and session state for the portal."""

    def __init__(self, username: str, password: str, base_url: str):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.is_authenticated = False
        self._session_cookies: dict[str, str] = {}
        self._auth_headers: dict[str, str] = {}

    async def authenticate(self, client: httpx.AsyncClient) -> bool:
        """Execute login flow against legacy portal per PROTOCOL.md."""
        raise NotImplementedError(
            "Authentication flow will be implemented based on PROTOCOL.md facts."
        )

    def apply_auth(self, request: httpx.Request) -> httpx.Request:
        """Inject active session cookies and headers into outgoing portal requests."""
        for name, value in self._session_cookies.items():
            request.headers.append("cookie", f"{name}={value}")
        for header, value in self._auth_headers.items():
            request.headers[header] = value
        return request

    def invalidate_session(self) -> None:
        """Clear cached session tokens and cookies on 401/expiry."""
        self.is_authenticated = False
        self._session_cookies.clear()
        self._auth_headers.clear()
