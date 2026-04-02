import sys

from loguru import logger
from app.core.config import settings


LOGURU_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)


def setup_logging() -> None:
    """Configure loguru for the application.

    - DEBUG/INFO: colored console output (development)
    - WARNING+: use serialize=True → clean one-JSON-line-per-log
    """
    logger.remove()

    if settings.log_level in ("DEBUG", "INFO"):
        logger.add(
            sys.stderr,
            format=LOGURU_FORMAT,
            level=settings.log_level,
            colorize=True,
        )
    else:
        # serialize=True produces clean JSON lines without format-string escaping issues
        logger.add(
            sys.stderr,
            level=settings.log_level,
            serialize=True,
        )

    # Gate uvicorn's built-in logging to avoid double-output
    import logging
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)


# Shared application logger — import this everywhere
app_logger = logger.bind(name="swiss-ephemeris-api")
