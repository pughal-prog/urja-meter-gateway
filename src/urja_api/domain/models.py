"""Domain models representing clean smart-meter entities.

All dates are represented in ISO-8601 UTC. Units are explicit.
These models are completely isolated from legacy portal quirks.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class MeterStatus(StrEnum):
    """Operational status of a smart meter."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    FAULT = "FAULT"
    DISCONNECTED = "DISCONNECTED"
    UNKNOWN = "UNKNOWN"


class Location(BaseModel):
    """Geographic and administrative location coordinates."""

    model_config = ConfigDict(extra="forbid")

    latitude: float | None = Field(default=None, description="WGS84 latitude coordinate")
    longitude: float | None = Field(default=None, description="WGS84 longitude coordinate")
    address: str | None = Field(default=None, description="Physical site address")
    city: str | None = Field(default=None, description="City or administrative area")
    substation: str | None = Field(default=None, description="Electrical substation name")
    feeder: str | None = Field(default=None, description="Associated distribution feeder name")


class Reading(BaseModel):
    """Instantaneous meter reading at a specific point in time."""

    model_config = ConfigDict(extra="forbid")

    timestamp: datetime = Field(..., description="Timestamp of reading in UTC ISO-8601")
    energy_kwh: float = Field(..., description="Cumulative active energy in kWh")
    voltage_v: float | None = Field(default=None, description="Line voltage in Volts")
    current_a: float | None = Field(default=None, description="Current in Amperes")
    power_factor: float | None = Field(default=None, description="Power factor (0.0 to 1.0)")


class Consumption(BaseModel):
    """Aggregated energy consumption over a time window."""

    model_config = ConfigDict(extra="forbid")

    meter_id: str = Field(..., description="Unique meter identifier")
    start_time: datetime = Field(..., description="Start of window in UTC ISO-8601")
    end_time: datetime = Field(..., description="End of window in UTC ISO-8601")
    granularity: str = Field(
        default="hourly",
        description="Granularity of aggregation (hourly, daily, monthly)",
    )
    readings_count: int = Field(
        default=0,
        description="Number of samples included in this window",
    )


class Meter(BaseModel):
    """Canonical representation of a smart meter."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="Unique system-wide meter identifier")
    serial_number: str = Field(
        ...,
        description="Hardware serial number displayed on physical device",
    )
    status: MeterStatus = Field(
        default=MeterStatus.UNKNOWN,
        description="Current operational status",
    )
    location: Location | None = Field(default=None, description="Physical and network location")
    installed_at: datetime | None = Field(default=None, description="Installation timestamp in UTC")
    last_reading_at: datetime | None = Field(
        default=None,
        description="Timestamp of last received reading in UTC",
    )


class Node(BaseModel):
    """Grid hierarchy tree node (e.g. Substation -> Feeder -> Transformer -> Meter)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="Unique node identifier")
    name: str = Field(..., description="Display label or asset identifier")
    node_type: str = Field(
        ...,
        description="Level in grid hierarchy (substation, feeder, transformer, meter)",
    )
    parent_id: str | None = Field(default=None, description="Identifier of parent node in topology")
    children: list["Node"] = Field(default_factory=list, description="Child nodes in topology")
