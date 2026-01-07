from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Literal

import yaml
from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def _load_yaml_settings(env_name: str) -> Dict[str, Any]:
    config_path = Path("config") / f"{env_name}.yaml"
    if not config_path.exists():
        return {}
    raw = config_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid config format in {config_path}")
    return data


def _read_env_name() -> str:
    direct = os.getenv("ENV") or os.getenv("APP_ENV")
    if direct:
        return direct
    env_path = Path(".env")
    if not env_path.exists():
        return "dev"
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("ENV="):
            return line.split("=", 1)[1].strip()
        if line.startswith("APP_ENV="):
            return line.split("=", 1)[1].strip()
    return "dev"


class Settings(BaseSettings):
    """Application configuration loaded from environment, .env, and YAML."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True,
    )

    env_name: str = Field(default="dev", validation_alias=AliasChoices("ENV", "APP_ENV"))
    base_url: str = Field(validation_alias=AliasChoices("APP_BASE_URL", "base_url"))
    timeout: int = Field(default=10000, validation_alias=AliasChoices("APP_TIMEOUT", "timeout"))
    headless: bool = Field(default=True, validation_alias=AliasChoices("APP_HEADLESS", "headless"))
    browser: Literal["chromium", "firefox"] = Field(
        default="chromium",
        validation_alias=AliasChoices("APP_BROWSER", "browser"),
    )
    app_username: SecretStr = Field(
        validation_alias=AliasChoices("APP_USERNAME", "app_username")
    )
    app_password: SecretStr = Field(
        validation_alias=AliasChoices("APP_PASSWORD", "app_password")
    )
    trace_mode: Literal["off", "on", "retain-on-failure"] = Field(
        default="retain-on-failure",
        validation_alias=AliasChoices("APP_TRACE_MODE", "trace_mode"),
    )
    video_mode: Literal["off", "retain-on-failure"] = Field(
        default="off",
        validation_alias=AliasChoices("APP_VIDEO_MODE", "video_mode"),
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        env_name = _read_env_name()
        yaml_data = _load_yaml_settings(str(env_name))

        def yaml_settings() -> Dict[str, Any]:
            return yaml_data

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            yaml_settings,
            file_secret_settings,
        )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings loaded from environment or .env."""
    return Settings()
