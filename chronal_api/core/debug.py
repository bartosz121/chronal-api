import logging
import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from chronal_api.core.config import get_config

config = get_config()

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

request_uuid_ctx = ContextVar("REQUEST_UUID", default=None)


@contextmanager
def request_uuid_context():
    request_uuid = str(uuid.uuid4())
    token = request_uuid_ctx.set(request_uuid)
    yield
    request_uuid_ctx.reset(token)


class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        t = time.monotonic()
        response = await call_next(request)
        elapsed = time.monotonic() - t
        response.headers["X-Process-Time"] = str(elapsed)
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        with request_uuid_context():
            req_url = request.url.path
            request_uuid = request_uuid_ctx.get()
            logging.info("[%s] Incoming request to %s", request_uuid, repr(req_url))
            try:
                response = await call_next(request)
                response.headers["X-Request-UUID"] = request_uuid
            except Exception as exc:
                logging.error(
                    "[%s] Request to %s failed: %s", request_uuid, repr(req_url), exc
                )
                raise exc
            else:
                logging.info(
                    "[%s] Successful request to %s", request_uuid, repr(req_url)
                )
                if config.IS_DEV:
                    logging.debug(
                        "[%s] Response headers: %s", request_uuid, response.headers
                    )
                return response
