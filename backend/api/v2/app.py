import typing
import uuid
from contextlib import asynccontextmanager
import uvicorn

import httpx
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v2 import routers
from backend.api.loguru_logger.log_config import logger_setup
from backend.api.v2.middleware import add_http_middleware
from backend.api.v2.exc import exception_handlers as exc
from loguru import logger

@asynccontextmanager
async def lifespan(func_app: FastAPI) -> typing.AsyncContextManager[None]:
    logger_setup()
    # PostgresSessionManager.init_db(database=databases["postgres"])
    # db_manager = PostgresSessionManager(database=databases["postgres"])
    func_app.requests_client = httpx.AsyncClient()
    yield
    await func_app.requests_client.aclose()
    # if db_manager.engine is not None:
    # Close the DB connection
    # await db_manager.close()


_app = FastAPI(lifespan=lifespan, root_path="")
add_http_middleware(app=_app)

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

_app = exc.add_exception_handlers(app=_app)
_app.include_router(router=routers.about)
_app.include_router(router=routers.healthcheck)
_app.include_router(router=routers.rbac)
_app.include_router(router=routers.api_exceptions_router)
_app.include_router(router=routers.db_exceptions_router)
_app.include_router(router=routers.db_router)
_app.include_router(router=routers.delay_router)


v2_app = _app


if __name__ == "__main__":
    """
    Necessary for pycharm debugging purposes.
    If we run your module imported by another (including gunicorn) using something like:
    from manage import app then the value is 'app' or 'manage.app'
    """
    logger.info("V2 started")
    uvicorn.run(
        "app:v2_app",
        host="0.0.0.0",
        port=8762,
        log_config=None,
        access_log=False,
    )
