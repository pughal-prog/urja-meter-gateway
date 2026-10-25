"""Smart meter endpoints: listing, lookup, and consumption analytics."""

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from urja_api.api.deps import get_consumption_service, get_meter_service
from urja_api.domain.models import Consumption, Meter
from urja_api.services.consumption import ConsumptionService
from urja_api.services.meters import MeterService

router = APIRouter(prefix="/v1/meters", tags=["Meters"])


class PaginatedMetersResponse(BaseModel):
    """Paginated collection of meters."""

    items: list[Meter] = Field(default_factory=list, description="Meters matching search criteria")
    total: int = Field(default=0, description="Total number of matching meters")
    limit: int = Field(default=50, description="Page limit")
    offset: int = Field(default=0, description="Page offset")


@router.get("", response_model=PaginatedMetersResponse, summary="List or search smart meters")
async def list_meters(
    query: str | None = Query(default=None, description="Search by serial number or location"),
    status: str | None = Query(default=None, description="Filter by operational status"),
    limit: int = Query(default=50, ge=1, le=500, description="Maximum items to return"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    meter_service: MeterService = Depends(get_meter_service),
) -> PaginatedMetersResponse:
    """List or search smart meters with filtering and pagination."""
    meters = await meter_service.list_meters(
        query=query, status=status, limit=limit, offset=offset
    )
    return PaginatedMetersResponse(items=meters, total=len(meters), limit=limit, offset=offset)


@router.get("/{meter_id}", response_model=Meter, summary="Get smart meter details")
async def get_meter(
    meter_id: str,
    meter_service: MeterService = Depends(get_meter_service),
) -> Meter:
    """Retrieve detailed metadata and location for a specific smart meter."""
    return await meter_service.get_meter(meter_id=meter_id)


@router.get(
    "/{meter_id}/consumption",
    response_model=list[Consumption],
    summary="Get meter energy consumption",
)
async def get_meter_consumption(
    meter_id: str,
    from_time: datetime = Query(..., alias="from", description="Start timestamp in ISO-8601 UTC"),
    to_time: datetime = Query(..., alias="to", description="End timestamp in ISO-8601 UTC"),
    granularity: str = Query(
        default="hourly",
        pattern="^(hourly|daily|monthly)$",
        description="Aggregation granularity",
    ),
    consumption_service: ConsumptionService = Depends(get_consumption_service),
) -> list[Consumption]:
    """Retrieve aggregated consumption time-series for a smart meter."""
    return await consumption_service.get_consumption(
        meter_id=meter_id,
        start_time=from_time,
        end_time=to_time,
        granularity=granularity,
    )
