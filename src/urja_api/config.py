"""Application configuration and environment settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global configuration settings for the Urja Meter API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Portal connection settings
    portal_base_url: str = Field(
        default="https://portal.urjameterops.example.com",
        description="Base URL for the legacy Urja Meter Ops web portal",
    )
    portal_username: str = Field(
        default="",
        description="Portal authentication username",
    )
    portal_password: str = Field(
        default="",
        description="Portal authentication password",
    )

    # Portal client policies
    portal_rate_limit_rps: float = Field(
        default=2.0,
        description="Maximum requests per second allowed to the legacy portal",
    )
    portal_timeout_seconds: float = Field(
        default=15.0,
        description="HTTP request timeout in seconds",
    )
    portal_max_retries: int = Field(
        default=3,
        description="Maximum retry attempts on transient portal failures",
    )

    # Application settings
    app_host: str = Field(default="0.0.0.0", description="API host")
    app_port: int = Field(default=8000, description="API port")
    app_env: str = Field(
        default="development",
        description="Environment (development, test, production)",
    )
    log_level: str = Field(default="INFO", description="Log level")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
