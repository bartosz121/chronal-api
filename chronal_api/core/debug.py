import logging
import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar

from fastapi import Request, Response

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

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

REQUEST_UUID = ContextVar("REQUEST_UUID", default=None)


@contextmanager
def request_uuid_context():
    request_uuid = str(uuid.uuid4())
    token = REQUEST_UUID.set(request_uuid)
    yield
    REQUEST_UUID.reset(token)


class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        t = time.monotonic()
        response = await call_next(request)
        elapsed = time.monotonic() - t
        response.headers["X-Process-Time"] = str(elapsed)
        return response


class RequestUUIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        with request_uuid_context():
            response = await call_next(request)
            request_uuid = REQUEST_UUID.get()
            response.headers["X-Request-UUID"] = request_uuid
            logging.debug(
                "[%s] %s %s",
                request_uuid,
                request.url,
                response.headers,
            )
            return response
