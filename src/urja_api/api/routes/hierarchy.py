"""Grid hierarchy and electrical topology routes."""

from fastapi import APIRouter, Depends

from urja_api.api.deps import get_hierarchy_service
from urja_api.domain.models import Node
from urja_api.services.hierarchy import HierarchyService

router = APIRouter(prefix="/v1/hierarchy", tags=["Hierarchy"])


@router.get("", response_model=list[Node], summary="Get electrical grid hierarchy tree")
async def get_hierarchy(
    hierarchy_service: HierarchyService = Depends(get_hierarchy_service),
) -> list[Node]:
    """Retrieve full electrical distribution hierarchy from substations to meters."""
    return await hierarchy_service.get_hierarchy_tree()


@router.get(
    "/meters/{meter_id}/ancestors",
    response_model=list[Node],
    summary="Get meter electrical path",
)
async def get_meter_ancestors(
    meter_id: str,
    hierarchy_service: HierarchyService = Depends(get_hierarchy_service),
) -> list[Node]:
    """Retrieve upstream chain of supply (feeder, transformer, substation) for a meter."""
    return await hierarchy_service.get_meter_ancestors(meter_id=meter_id)
