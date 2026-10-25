"""Parsers to convert raw portal responses (JSON/HTML) into clean domain representations.

Isolates all format anomalies, missing fields, idiosyncratic keys, and date formats.
Strictly implemented according to PROTOCOL.md once facts are discovered.
"""

from typing import Any

from urja_api.domain.models import Meter, Node, Reading


class PortalParser:
    """Transforms legacy portal raw payloads into typed domain structures."""

    @staticmethod
    def parse_meter_list(raw_data: Any) -> list[Meter]:
        """Parse raw response from meter list/search endpoint."""
        raise NotImplementedError("Will be implemented in Phase 3 per PROTOCOL.md.")

    @staticmethod
    def parse_meter_detail(raw_data: Any) -> Meter:
        """Parse raw response from meter detail endpoint."""
        raise NotImplementedError("Will be implemented in Phase 3 per PROTOCOL.md.")

    @staticmethod
    def parse_readings(raw_data: Any) -> list[Reading]:
        """Parse raw consumption/readings response."""
        raise NotImplementedError("Will be implemented in Phase 3 per PROTOCOL.md.")

    @staticmethod
    def parse_hierarchy(raw_data: Any) -> list[Node]:
        """Parse raw grid hierarchy/topology response."""
        raise NotImplementedError("Will be implemented in Phase 3 per PROTOCOL.md.")
