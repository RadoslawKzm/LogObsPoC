import typing
import uuid
from contextlib import asynccontextmanager

import httpx
import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend import exceptions
from backend.api.config import settings
from backend.loguru_logger.log_config import logger_setup

from . import routers


@asynccontextmanager
async def lifespan(func_app: FastAPI) -> typing.AsyncContextManager[None]:
    logger_setup(settings=settings)
    # PostgresSessionManager.init_db(database=databases["postgres"])
    # db_manager = PostgresSessionManager(database=databases["postgres"])
    func_app.requests_client = httpx.AsyncClient()
    yield
    await func_app.requests_client.aclose()
    # if db_manager.engine is not None:
    # Close the DB connection
    # await db_manager.close()


_app = FastAPI(lifespan=lifespan, root_path="")


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

_app = exceptions.add_handlers(app=_app)
_app.include_router(router=routers.about)
_app.include_router(router=routers.health)
_app.include_router(router=routers.rbac)
_app.include_router(router=routers.exceptions)
_app.include_router(router=routers.db)
_app.include_router(router=routers.delay)


v1_app = _app
logger.info(
    f"V1 link: "
    f"http://{settings.API_HOST}:{settings.API_PORT}/api/v1{v1_app.docs_url}"
)


if __name__ == "__main__":
    """
    Necessary for pycharm debugging purposes.
    If we run your module imported by another
        (including gunicorn) using something like:
    from manage import app then the value is 'app' or 'manage.app'
    """
    logger.info("V1 started")
    uvicorn.run(
        app=v1_app,
        host="0.0.0.0",
        port=8761,
        log_config=None,
        access_log=False,
    )
