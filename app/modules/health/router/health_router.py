from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.postgres import get_db_session
from app.infra.logger import get_logger
from app.modules.health.schemas.health_response import HealthResponse
from app.modules.health.service.health_service import HealthService

router = APIRouter(prefix="/health", tags=["health"])
logger = get_logger(__name__)

DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/", response_model=HealthResponse)
async def health_check(
    db: DbSessionDep,
) -> HealthResponse:
    logger.info("Health check requested.")

    service = HealthService()

    postgres_ok = await service.check_postgres(db)
    redis_ok = await service.check_redis()

    status = "ok" if postgres_ok and redis_ok else "degraded"
    postgres_status = "ok" if postgres_ok else "fail"
    redis_status = "ok" if redis_ok else "fail"

    logger.info(
        "Health check result: status=%s, postgres=%s, redis=%s",
        status,
        postgres_status,
        redis_status,
    )

    return HealthResponse(
        status=status,
        postgres=postgres_status,
        redis=redis_status,
    )
