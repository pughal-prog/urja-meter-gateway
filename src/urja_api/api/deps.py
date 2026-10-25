"""FastAPI dependency injection providers."""

from fastapi import Depends

from urja_api.config import Settings, get_settings
from urja_api.portal.client import PortalClient
from urja_api.services.consumption import ConsumptionService
from urja_api.services.hierarchy import HierarchyService
from urja_api.services.meters import MeterService

# Singleton portal client instance managed across app lifespan
_portal_client: PortalClient | None = None


def get_portal_client(settings: Settings = Depends(get_settings)) -> PortalClient:
    """Provide singleton PortalClient instance."""
    global _portal_client
    if _portal_client is None:
        _portal_client = PortalClient(settings)
    return _portal_client


def get_meter_service(client: PortalClient = Depends(get_portal_client)) -> MeterService:
    """Provide MeterService instance."""
    return MeterService(client)


def get_consumption_service(
    client: PortalClient = Depends(get_portal_client),
) -> ConsumptionService:
    """Provide ConsumptionService instance."""
    return ConsumptionService(client)


def get_hierarchy_service(client: PortalClient = Depends(get_portal_client)) -> HierarchyService:
    """Provide HierarchyService instance."""
    return HierarchyService(client)
