"""Meter service implementing meter retrieval and search business logic."""

from urja_api.domain.models import Meter
from urja_api.portal.client import PortalClient


class MeterService:
    """Service handling meter listing, search, and detail resolution."""

    def __init__(self, portal_client: PortalClient):
        self.portal_client = portal_client

    async def list_meters(
        self,
        query: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Meter]:
        """Retrieve paginated meters matching optional search and filter criteria."""
        raise NotImplementedError("Will be implemented in Phase 4.")

    async def get_meter(self, meter_id: str) -> Meter:
        """Retrieve detailed information for a specific meter by ID."""
        raise NotImplementedError("Will be implemented in Phase 4.")
