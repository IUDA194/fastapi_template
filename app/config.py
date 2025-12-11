from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

TRUTHY_VALUES = {"1", "true", "yes", "on"}


def _to_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in TRUTHY_VALUES


def _running_tests() -> bool:
    return bool(
        os.getenv("PYTEST_CURRENT_TEST") or any("pytest" in arg.lower() for arg in sys.argv)
    )


def _resolve_env_file() -> str | None:
    if not _to_bool(os.getenv("SETTINGS_USE_ENV_FILE"), default=True):
        return None

    if _running_tests() and not _to_bool(
        os.getenv("SETTINGS_USE_ENV_FILE_IN_TESTS"),
        default=False,
    ):
        return None

    env_file = os.getenv("SETTINGS_ENV_FILE", ".env").strip()
    if not env_file:
        return None

    env_path = Path(env_file)
    if not env_path.exists():
        return None

    return str(env_path)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    APP_NAME: str = "FastAPI Service"
    DEBUG: bool = False

    # API
    API_PREFIX: str = "/api"

    # Database (Postgres)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/app_db",
        description="SQLAlchemy async DB URL",
    )

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Кэшируем настройки, чтобы не пересоздавать объект Settings.
    Pydantic Settings сам подхватывает переменные из окружения или .env.
    """
    env_file = _resolve_env_file()
    init_kwargs: dict[str, Any] = {}
    if env_file:
        init_kwargs["_env_file"] = env_file
        init_kwargs["_env_file_encoding"] = "utf-8"

    settings = Settings(**init_kwargs)

    module_logger = globals().get("logger")
    if module_logger:
        module_logger.debug(
            "Settings initialized (debug=%s, prefix=%s).",
            settings.DEBUG,
            settings.API_PREFIX,
        )

    return settings
