from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.infra.logger import get_logger
from app.modules.health.router.health_router import router as health_router

logger = get_logger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info("Application startup complete.")
    try:
        yield
    finally:
        logger.info("Application shutdown.")


def create_app() -> FastAPI:
    """
    Application factory so tests and ASGI servers reuse the same setup.
    """
    settings = get_settings()

    logger.debug("Creating FastAPI application instance.")
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=app_lifespan,
    )

    app.include_router(health_router)

    return app


app = create_app()
logger.debug("App main module loaded and FastAPI app created.")
