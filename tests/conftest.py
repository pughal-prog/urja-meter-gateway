"""Pytest configuration and shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from urja_api.config import Settings, get_settings
from urja_api.main import create_app


@pytest.fixture
def test_settings() -> Settings:
    """Return test settings with dummy credentials and base URL."""
    return Settings(
        portal_base_url="https://portal-mock.urjameterops.test",
        portal_username="test_user",
        portal_password="test_password",
        portal_rate_limit_rps=100.0,
        portal_timeout_seconds=2.0,
        portal_max_retries=2,
        app_env="test",
    )


@pytest.fixture
def app(test_settings: Settings):
    """FastAPI application instance for testing."""
    application = create_app()
    application.dependency_overrides[get_settings] = lambda: test_settings
    yield application
    application.dependency_overrides.clear()


@pytest.fixture
def test_client(app) -> TestClient:
    """Synchronous test client for API endpoints."""
    return TestClient(app)
