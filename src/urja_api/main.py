"""FastAPI application factory, lifespan management, and router mounting."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from urja_api.api.deps import _portal_client
from urja_api.api.routes import health, hierarchy, meters
from urja_api.config import get_settings
from urja_api.errors import register_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycles."""
    # Validate settings on startup
    _ = get_settings()
    yield
    # Shutdown actions
    if _portal_client is not None:
        await _portal_client.close()


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""
    app = FastAPI(
        title="Urja Meter Ops API",
        summary="A clean, typed REST API wrapper in front of legacy Urja Meter Ops portal",
        description=(
            "Provides standardized, resource-oriented access to smart meters, "
            "readings, energy consumption analytics, and electrical grid hierarchy."
        ),
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Register error handlers
    register_error_handlers(app)

    # Mount routers
    app.include_router(health.router)
    app.include_router(meters.router)
    app.include_router(hierarchy.router)

    return app


app = create_app()
