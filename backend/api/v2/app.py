import typing
import uuid
from contextlib import asynccontextmanager

import httpx
import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from loguru import logger

from backend.api.config import settings
from backend.api.v2 import routers
from backend.exceptions import exception_handlers as exc
from backend.loguru_logger.log_config import logger_setup


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


_app = FastAPI(
    lifespan=lifespan,
    root_path="",
    default_response_class=ORJSONResponse,
)


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
_app.include_router(router=routers.health)
_app.include_router(router=routers.files_router)
_app.include_router(router=routers.users_router)
_app.include_router(router=routers.workspaces_router)
_app.include_router(router=routers.tasks_router)


v2_app = _app
logger.info(
    f"V2 link: "
    f"http://{settings.API_HOST}:{settings.API_PORT}/api/v2{v2_app.docs_url}"
)

if __name__ == "__main__":
    """
    Necessary for pycharm debugging purposes.
    If we run your module imported by another
        (including gunicorn) using something like:
    from manage import app then the value is 'app' or 'manage.app'
    """
    logger.info("V2 started")
    logger.info(f"V2 link: " f"http://0.0.0.0:8762/api/v2{v2_app.docs_url}")
    uvicorn.run(
        app=v2_app,
        host="0.0.0.0",
        port=8762,
        log_config=None,
        access_log=False,
    )
