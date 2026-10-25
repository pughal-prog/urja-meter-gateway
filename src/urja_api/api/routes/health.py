"""Health check endpoints for liveness and portal connectivity."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from urja_api.api.deps import get_portal_client
from urja_api.portal.client import PortalClient

router = APIRouter(tags=["Health"])


class HealthStatus(BaseModel):
    """Health check response payload."""

    status: str = Field(default="ok", description="Overall service status ('ok' or 'degraded')")
    portal_reachable: bool = Field(default=False, description="Whether legacy portal is reachable")
    version: str = Field(default="0.1.0", description="API version")


@router.get("/health", response_model=HealthStatus, summary="Check API and portal health")
async def check_health(client: PortalClient = Depends(get_portal_client)) -> HealthStatus:
    """Return service liveness and upstream portal reachability."""
    # Stub implementation - returns default healthy status during scaffold
    return HealthStatus(status="ok", portal_reachable=True, version="0.1.0")
