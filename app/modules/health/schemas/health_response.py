from pydantic import BaseModel

from app.infra.logger.logger import get_logger

logger = get_logger(__name__)
logger.debug("HealthResponse schema defined.")


class HealthResponse(BaseModel):
    status: str
    postgres: str
    redis: str
