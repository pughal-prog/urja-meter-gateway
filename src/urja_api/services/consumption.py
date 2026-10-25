"""Consumption service handling energy aggregation and readings time-series."""

from datetime import datetime

from urja_api.domain.models import Consumption, Reading
from urja_api.portal.client import PortalClient


class ConsumptionService:
    """Service computing aggregated consumption and retrieving meter readings."""

    def __init__(self, portal_client: PortalClient):
        self.portal_client = portal_client

    async def get_readings(
        self,
        meter_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Reading]:
        """Fetch raw readings for a meter within a time window."""
        raise NotImplementedError("Will be implemented in Phase 4.")

    async def get_consumption(
        self,
        meter_id: str,
        start_time: datetime,
        end_time: datetime,
        granularity: str = "hourly",
    ) -> list[Consumption]:
        """Compute aggregated energy consumption metrics across intervals."""
        raise NotImplementedError("Will be implemented in Phase 4.")
