import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        if level in {"WARNING", "ERROR", "CRITICAL"}:
            logger.opt(exception=record.exc_info).log(level, record.getMessage())


# Remove default handlers
logging.root.handlers = []
logging.root.setLevel(logging.WARNING)
logging.basicConfig(handlers=[InterceptHandler()])

# Redirect Gunicorn loggers to Loguru
for name in (
    "gunicorn",
    "gunicorn.access",
    "gunicorn.error",
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
):
    logging.getLogger(name).handlers = [InterceptHandler()]
    logging.getLogger(name).propagate = False
