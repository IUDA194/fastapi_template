from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.cache.redis import check_redis
from app.infra.logger.logger import logger


class HealthService:
    async def check_postgres(self, session: AsyncSession) -> bool:
        logger.debug("Checking Postgres availability.")
        try:
            # ВАЖНО: оборачиваем строку в text()
            await session.execute(text("SELECT 1"))
            return True
        except Exception:
            logger.exception("Postgres health check failed.")
            return False

    async def check_redis(self) -> bool:
        logger.debug("Checking Redis availability.")
        ok = await check_redis()
        if ok:
            logger.debug("Redis health check succeeded.")
        else:
            logger.error("Redis health check failed.")
        return ok
