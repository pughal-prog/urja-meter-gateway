"""Domain errors and standardized FastAPI exception handlers."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Structured error payload returned by all API endpoints."""

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    details: dict[str, Any] | None = Field(
        default=None,
        description="Additional context or validation details",
    )


class DomainError(Exception):
    """Base class for all domain-specific errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class PortalError(DomainError):
    """Raised when communication with the legacy portal fails."""

    def __init__(
        self,
        message: str,
        code: str = "PORTAL_ERROR",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, code=code, details=details)


class PortalAuthError(PortalError):
    """Raised when portal credentials or session tokens fail."""

    def __init__(
        self,
        message: str = "Portal authentication failed",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, code="PORTAL_AUTH_FAILED", details=details)


class PortalRateLimitError(PortalError):
    """Raised when portal requests are being throttled."""

    def __init__(
        self,
        message: str = "Portal rate limit exceeded",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, code="PORTAL_RATE_LIMIT", details=details)


class ResourceNotFoundError(DomainError):
    """Raised when a requested resource (e.g., meter) is not found."""

    def __init__(self, message: str, resource_type: str, resource_id: str):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": resource_id},
        )


def register_error_handlers(app: FastAPI) -> None:
    """Register uniform exception handlers on the FastAPI application."""

    @app.exception_handler(ResourceNotFoundError)
    async def not_found_handler(request: Request, exc: ResourceNotFoundError) -> JSONResponse:
        payload = ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload.model_dump())

    @app.exception_handler(PortalAuthError)
    async def portal_auth_handler(request: Request, exc: PortalAuthError) -> JSONResponse:
        payload = ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content=payload.model_dump())

    @app.exception_handler(PortalError)
    async def portal_error_handler(request: Request, exc: PortalError) -> JSONResponse:
        payload = ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content=payload.model_dump())

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        payload = ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload.model_dump())
