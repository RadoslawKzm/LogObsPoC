import fastapi
from fastapi.requests import Request
from loguru import logger

from . import api_exceptions, db_exceptions
from .base_exception import BaseCustomException


def add_exception_handlers(app: fastapi.FastAPI) -> fastapi.FastAPI:
    @app.exception_handler(api_exceptions.ApiException)
    async def api_exception_handler(
        request: Request,
        exc: api_exceptions.ApiException,
    ) -> fastapi.responses.JSONResponse:
        logger.opt(lazy=True, exception=exc).error(
            lambda: f"Internal message: {exc.internal_message}, "
            f"Internal code: {exc.internal_code}"
        )
        return fastapi.responses.JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(db_exceptions.DbException)
    async def db_exception_handler(
        request: Request,
        exc: db_exceptions.DbException,
    ) -> fastapi.responses.JSONResponse:
        logger.opt(lazy=True, exception=exc).error(
            lambda: f"Internal message: {exc.internal_message}, "
            f"Internal code: {exc.internal_code}"
        )
        return fastapi.responses.JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(BaseCustomException)
    async def custom_exception_handler(
        request: Request,
        exc: BaseCustomException,
    ) -> fastapi.responses.JSONResponse:
        logger.opt(lazy=True, exception=exc).error(
            lambda: f"Internal message: {exc.internal_message}, "
            f"Internal code: {exc.internal_code}"
        )
        return fastapi.responses.JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
            headers={},
        )

    @app.exception_handler(Exception)
    async def custom_generic_handler(
        request: Request,
        exc: Exception,
    ) -> fastapi.responses.JSONResponse:
        logger.opt(lazy=True, exception=exc).error(f"Unhandled Exception.")
        return fastapi.responses.JSONResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Team got notified and working on solution."},
            headers={},
        )

    return app
