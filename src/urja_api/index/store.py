"""SQLite local indexing store for attribute filtering and proximity queries."""

from pathlib import Path

from urja_api.domain.models import Meter


class SQLiteIndexStore:
    """Manages local SQLite database schema and meter index queries."""

    def __init__(self, db_path: Path | str = "meters_index.sqlite"):
        self.db_path = str(db_path)

    async def init_schema(self) -> None:
        """Initialize SQLite tables, indexes, and schema migrations."""
        raise NotImplementedError("Will be implemented in Phase 6 extension.")

    async def upsert_meters(self, meters: list[Meter]) -> int:
        """Insert or update batch of meters in local index."""
        raise NotImplementedError("Will be implemented in Phase 6 extension.")

    async def find_near_location(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        limit: int = 50,
    ) -> list[Meter]:
        """Find meters within radius using bounding-box or Haversine distance formula."""
        raise NotImplementedError("Will be implemented in Phase 6 extension.")
