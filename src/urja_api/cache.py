"""In-memory TTL cache with explicit staleness and eviction policies."""

import time
from typing import Any


class TTLCache:
    """Lightweight in-memory cache with explicit time-to-live per key."""

    def __init__(self, default_ttl_seconds: int = 300):
        self.default_ttl_seconds = default_ttl_seconds
        self._cache: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        """Retrieve value if key exists and has not expired."""
        if key not in self._cache:
            return None
        expires_at, val = self._cache[key]
        if time.time() > expires_at:
            del self._cache[key]
            return None
        return val

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        """Store value with expiration timestamp."""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        self._cache[key] = (time.time() + ttl, value)

    def clear(self) -> None:
        """Evict all entries."""
        self._cache.clear()
