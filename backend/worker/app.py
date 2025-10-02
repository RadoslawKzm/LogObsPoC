import time
import typing
import uuid
import contextlib
import asyncio

import fastapi
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.worker.health_check import health_router
from backend.loguru_logger.log_config import logger_setup
from backend.worker.config import worker_settings
from backend.worker.core.main import rabbit_worker
from backend.rabbit import init_rabbit


logger.info("App is loading!")
logger.info("Waiting for application startup.")



@contextlib.asynccontextmanager
async def lifespan(func_app: FastAPI) -> typing.AsyncContextManager[None]:
    logger_setup(worker_settings)
    logger.info("Starting lifespan processes...")

    # Initialize Rabbit
    conn, ch = await init_rabbit(settings=worker_settings)
    func_app.state.rabbit_connection = conn
    func_app.state.rabbit_channel = ch

    logger.info("Starting RabbitMQ background task")
    func_app.state.worker_task = asyncio.create_task(
        rabbit_worker(conn, worker_settings.WORKER_RABBIT_QUEUE)
    )

    logger.info("Application startup complete.")
    app_link: str = (
        f"http://{worker_settings.WORKER_API_HOST}:{worker_settings.WORKER_API_PORT}/api{func_app.docs_url}"
    )
    logger.info(f"Uvicorn running on {app_link} (Press CTRL+C to quit)")

    yield

    logger.info("Lifespan processes shutdown...")
    # Graceful shutdown
    logger.info("Shutting down RabbitMQ worker...")
    func_app.state.worker_task.cancel()
    try:
        await func_app.state.worker_task
    except asyncio.CancelledError:
        pass

    await conn.close()

_app = FastAPI(lifespan=lifespan, root_path="/api")


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
        logger.log("ENTER", f"IN >> {request.method} {request.url.path}")
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    msg = f"<< OUT {response.status_code}: {duration:.3f}s"
    with logger.contextualize(
        method=request.method,
        path=request.url.path,
        response_code=response.status_code,
        duration=duration,
    ):
        if 200 <= response.status_code <= 299:
            logger.log("EXIT 200", msg)
        elif 300 <= response.status_code <= 399:
            logger.log("EXIT 300", msg)
        elif 400 <= response.status_code <= 499:
            logger.log("EXIT 400", msg)
        else:  # 500++
            logger.log("EXIT 500", msg)
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
logger.info("Initializing routers ...")
_app.include_router(router=health_router)
app = _app
