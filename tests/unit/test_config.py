from app.config import get_settings


def test_settings_default_values():
    settings = get_settings()
    assert settings.APP_NAME == "FastAPI Service"
    assert settings.API_PREFIX.startswith("/")
    assert "postgresql" in str(settings.DATABASE_URL)
    assert settings.REDIS_URL.startswith("redis://")


def test_settings_env_override(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://test:test@localhost:5432/test_db",
    )
    monkeypatch.setenv("APP_NAME", "Test App")

    get_settings.cache_clear()  # type: ignore[attr-defined]
    settings = get_settings()

    assert settings.APP_NAME == "Test App"
    assert "test_db" in str(settings.DATABASE_URL)

    get_settings.cache_clear()  # type: ignore[attr-defined]
