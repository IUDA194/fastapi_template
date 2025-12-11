from collections.abc import AsyncGenerator, Awaitable
from typing import cast

import redis.asyncio as redis

from app.config import get_settings
from app.infra.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis:
    """
    Ленивый синглтон Redis-клиента.
    """
    global _redis_client

    if _redis_client is None:
        logger.debug("Initializing Redis client.")
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    return _redis_client


async def get_redis_dep() -> AsyncGenerator[redis.Redis, None]:
    """
    Зависимость для FastAPI-хендлеров.
    """
    client = get_redis_client()
    yield client


async def check_redis() -> bool:
    """
    Health-check Redis: возвращает True, если PING прошёл успешно.
    """
    client = get_redis_client()
    try:
        logger.debug("Pinging Redis.")
        pong_awaitable: Awaitable[bool] = cast("Awaitable[bool]", client.ping())
        pong = await pong_awaitable
        logger.debug("Redis responded to PING with %s.", pong)
        return bool(pong)
    except Exception:
        logger.exception("Redis health check failed.")
        return False
