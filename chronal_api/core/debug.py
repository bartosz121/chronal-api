import time
import logging
from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "text": {
            "()": logging.Formatter,
            "format": "%(asctime)s.%(msecs)03d %(name)-30s %(levelname)-6s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "()": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "text",
        }
    },
    "root": {"level": logging.DEBUG, "handlers": ["console"]},
}


class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, next):
        t = time.monotonic()
        response = await next(request)
        elapsed = time.monotonic() - t
        response.headers["X-Process-Time"] = str(elapsed)
        return response
