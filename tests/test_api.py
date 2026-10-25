"""Tests for FastAPI endpoints (happy path and error responses)."""

from fastapi.testclient import TestClient


def test_health_endpoint(test_client: TestClient):
    """Verify /health returns 200 and expected status shape."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "portal_reachable" in data
    assert "version" in data
