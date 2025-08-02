import time
import typing
import uuid
from contextlib import asynccontextmanager

import fastapi
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.api import v1_app, v2_app
from backend.api.health_check import health_router
from backend.config import settings
from backend.loguru_logger.log_config import logger_setup
from backend.config import settings


@asynccontextmanager
async def lifespan(func_app: FastAPI) -> typing.AsyncContextManager[None]:
    logger_setup(settings)
    yield


_app = FastAPI(lifespan=lifespan, root_path="")


@_app.middleware("http")
async def log_requests(request: fastapi.Request, call_next):
    http_version = request.scope.get("http_version")
    with logger.contextualize(
        user_agent=request.headers["user-agent"] or "",
        client_ip=request.client.host,
        http_version=http_version,
        method=request.method,
        path=request.url.path,
    ):

        logger.log(
            "START",
            f"HTTP {http_version} Inbound:TOP | "
            f"{request.method} {request.url.path}",
        )
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    msg = (
        f"HTTP Outbound {request.method} {request.url.path} | "
        f"{response.status_code} {duration:.3f}s"
    )
    with logger.contextualize(
        method=request.method,
        path=request.url.path,
        response_code=response.status_code,
        duration=duration,
    ):
        if 200 <= response.status_code <= 299:
            logger.log("END 200", msg)
        elif 300 <= response.status_code <= 399:
            logger.log("END 300", msg)
        elif 400 <= response.status_code <= 499:
            logger.log("END 400", msg)
        else:  # 500++
            logger.log("END 500", msg)
    return response


_app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
    update_request_header=True,
    generator=lambda: uuid.uuid4().hex,
)

_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["X-Requested-With", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)

logger.info("Starting app")
logger.info("V1 initializing...")
_app.mount(path="/api/v1", app=v1_app)
logger.info("V2 initializing...")
_app.mount(path="/api/v2", app=v2_app)
logger.info("LATEST initializing...")
v2_app.include_router(health_router)
_app.mount(path="/api", app=v2_app)
logger.info("Application startup complete.")
app_link: str = (
    f"http://{settings.APP_HOST}:{settings.APP_PORT}/api{_app.docs_url}"
)
logger.info(f"Uvicorn running on {app_link} (Press CTRL+C to quit)")

app = _app
