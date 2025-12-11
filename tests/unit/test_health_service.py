# tests/unit/test_health_service.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.health.service.health_service import HealthService


class FakeSessionOK:
    """Фейковая AsyncSession, которая успешно выполняет execute()."""

    async def execute(self, query):
        return 1  # просто что-то


class FakeSessionFail:
    """Фейковая AsyncSession, у которой execute() падает."""

    async def execute(self, query):
        raise RuntimeError("DB is down")


@pytest.mark.asyncio
async def test_check_postgres_ok():
    service = HealthService()
    session: AsyncSession = FakeSessionOK()  # type: ignore[assignment]

    result = await service.check_postgres(session)
    assert result is True


@pytest.mark.asyncio
async def test_check_postgres_fail():
    service = HealthService()
    session: AsyncSession = FakeSessionFail()  # type: ignore[assignment]

    result = await service.check_postgres(session)
    assert result is False


@pytest.mark.asyncio
async def test_check_redis_ok(monkeypatch):
    service = HealthService()

    async def fake_check_redis_ok() -> bool:
        return True

    monkeypatch.setattr(
        "app.modules.health.service.health_service.check_redis",
        fake_check_redis_ok,
    )

    result = await service.check_redis()
    assert result is True


@pytest.mark.asyncio
async def test_check_redis_fail(monkeypatch):
    service = HealthService()

    async def fake_check_redis_fail() -> bool:
        return False

    monkeypatch.setattr(
        "app.modules.health.service.health_service.check_redis",
        fake_check_redis_fail,
    )

    result = await service.check_redis()
    assert result is False
