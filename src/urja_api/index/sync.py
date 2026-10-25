"""Synchronization service for bulk ingestion from portal to local index."""

from urja_api.index.store import SQLiteIndexStore
from urja_api.portal.client import PortalClient


class IndexSynchronizer:
    """Coordinates periodic or on-demand synchronization between portal and SQLite index."""

    def __init__(self, portal_client: PortalClient, store: SQLiteIndexStore):
        self.portal_client = portal_client
        self.store = store

    async def sync_all_meters(self) -> int:
        """Fetch all meters via bulk export / paginated listing and update local index."""
        raise NotImplementedError("Will be implemented in Phase 6 extension.")
