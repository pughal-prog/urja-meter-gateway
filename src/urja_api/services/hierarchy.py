"""Hierarchy service handling electrical grid topology tree reconstruction."""

from urja_api.domain.models import Node
from urja_api.portal.client import PortalClient


class HierarchyService:
    """Service responsible for reconstructing grid topology and resolving node trees."""

    def __init__(self, portal_client: PortalClient):
        self.portal_client = portal_client

    async def get_hierarchy_tree(self) -> list[Node]:
        """Construct hierarchical tree handling cycles, orphans, and duplicates explicitly."""
        raise NotImplementedError("Will be implemented in Phase 6 extension.")

    async def get_meter_ancestors(self, meter_id: str) -> list[Node]:
        """Trace path from root (Substation) to leaf (Meter)."""
        raise NotImplementedError("Will be implemented in Phase 6 extension.")
