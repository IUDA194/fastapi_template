import pytest

from app.config import get_settings


@pytest.mark.integration
@pytest.mark.asyncio
async def test_health_ok(async_client):
    """
    Интеграционный тест: реальный запрос к /health/.
    Требует живых Postgres и Redis с корректными DATABASE_URL и REDIS_URL.
    """
    settings = get_settings()

    assert settings.DATABASE_URL is not None
    assert settings.REDIS_URL is not None

    response = await async_client.get("/health/")
    assert response.status_code == 200

    data = response.json()
    assert set(data.keys()) == {"status", "postgres", "redis"}

    assert data["postgres"] in {"ok", "fail"}
    assert data["redis"] in {"ok", "fail"}
