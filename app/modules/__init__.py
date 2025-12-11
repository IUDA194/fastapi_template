from app.infra.logger.logger import get_logger
from app.modules.health.models import *  # noqa: F401,F403

__all__ = []

logger = get_logger(__name__)
logger.debug("Modules namespace initialized.")
