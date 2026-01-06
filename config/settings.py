from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    base_url: str = Field(validation_alias="APP_BASE_URL")
    timeout: int = Field(default=10000, validation_alias="APP_TIMEOUT")
    headless: bool = Field(default=True, validation_alias="APP_HEADLESS")
    browser: Literal["chromium", "firefox"] = Field(
        default="chromium",
        validation_alias="APP_BROWSER",
    )
    app_username: SecretStr = Field(validation_alias="APP_USERNAME")
    app_password: SecretStr = Field(validation_alias="APP_PASSWORD")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings loaded from environment or .env."""
    return Settings()
