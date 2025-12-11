import logging
import sys

from app.config import get_settings

settings = get_settings()


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"

    base_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    FORMATS = {
        logging.DEBUG: grey + base_format + reset,
        logging.INFO: green + base_format + reset,
        logging.WARNING: yellow + base_format + reset,
        logging.ERROR: red + base_format + reset,
        logging.CRITICAL: bold_red + base_format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.base_format)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def _create_handler(level: int) -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(CustomFormatter())
    return handler


def _configure_logger(name: str, level: int, handler: logging.Handler) -> logging.Logger:
    log = logging.getLogger(name)
    log.handlers.clear()
    log.setLevel(level)
    log.addHandler(handler)
    log.propagate = False
    return log


_level = logging.DEBUG if settings.DEBUG else logging.INFO
handler = _create_handler(_level)

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(logging.WARNING)


_app_logger = _configure_logger("fastapi_template", _level, handler)

for logger_name, logger_level in (
    ("sqlalchemy", logging.WARNING),
    ("sqlalchemy.engine", logging.INFO),
    ("sqlalchemy.engine.Engine", logging.INFO),
):
    _configure_logger(logger_name, logger_level, handler)

for logger_name in (
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
    "uvicorn.asgi",
    "uvicorn.lifespan",
):
    _configure_logger(logger_name, logging.INFO, handler)

logger = _app_logger


def get_logger(name: str) -> logging.Logger:
    """
    Получить дочерний логгер:
        log = get_logger(__name__)
    """
    return logger.getChild(name)
