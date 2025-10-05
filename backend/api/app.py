from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from backend.api import v1_app, v2_app
from backend.api.auth import auth_router
from backend.api.config import settings
from backend.api.health_check import health_router
from backend.loguru_logger import logger_setup
from backend.middleware import add_http_middleware
from backend.rabbit import declare_queues, init_rabbit

logger_setup(settings)


@asynccontextmanager
async def lifespan(func_app: FastAPI):
    # logger_setup(settings)
    logger.info("Starting lifespan processes...")
    _conn, _ch = await init_rabbit(settings=settings)
    await declare_queues(channel=_ch, settings=settings)
    # Store in the app state for health checks or shutdown handling
    # func_app.state.rabbit_connection = _conn
    # func_app.state.rabbit_channel = _ch
    v2_app.state.rabbit_connection = _conn
    v2_app.state.rabbit_channel = _ch
    yield


_app = FastAPI(lifespan=lifespan, root_path="")
add_http_middleware(_app=_app)


logger.info("Starting app")
logger.info("V1 initializing...")
_app.mount(path="/api/v1", app=v1_app)
logger.info("V2 initializing...")
_app.mount(path="/api/v2", app=v2_app)
logger.info("LATEST initializing...")
v2_app.include_router(health_router)
v2_app.include_router(auth_router)
_app.mount(path="/api", app=v2_app)

logger.info("Application startup complete.")
app_link: str = (
    f"http://{settings.API_HOST}:{settings.API_PORT}/api{_app.docs_url}"
)
logger.info(f"Uvicorn running on {app_link} (Press CTRL+C to quit)")

app = _app
