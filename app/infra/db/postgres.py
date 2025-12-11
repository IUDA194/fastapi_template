from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings
from app.infra.logger.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей.
    Наследуешься от него во всех модулях:
        class User(Base): ...
    """

    pass


engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
)
logger.debug("SQLAlchemy engine initialized (echo=%s).", settings.DEBUG)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
logger.debug("Database session factory configured.")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для FastAPI-хендлеров/сервисов.

        async def handler(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with SessionFactory() as session:
        logger.debug("Yielding database session.")
        try:
            yield session
        finally:
            logger.debug("Database session closed.")
