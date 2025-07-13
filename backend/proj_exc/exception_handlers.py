import traceback

import fastapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from loguru import logger
from backend.loguru_logger import safe_log

from backend.proj_exc.base import BaseCustomError

from . import api_exceptions, db_exceptions


def add_exception_handlers(app: fastapi.FastAPI) -> fastapi.FastAPI:
    @app.exception_handler(api_exceptions.ApiError)
    async def api_exception_handler(
        request: Request,
        exc: api_exceptions.ApiError,
    ):
        logger.critical("api_exceptions.ApiError is handled")
        tb = safe_log(traceback.format_exception(type(exc), exc, exc.__traceback__))
        logger.opt(exception=exc).error(
            f"Internal message: {exc.internal_message}, "
            f"Internal code: {exc.internal_code}, "
            f"HTTP response code: {exc.http_code}, "
            f"External message: {exc.external_message}, "
            f"Traceback: {tb}"
        )
        logger.critical(f"Response: {exc.external_message}")
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(db_exceptions.DbError)
    async def db_exception_handler(
        request: Request,
        exc: db_exceptions.DbError,
    ):
        logger.critical("db_exceptions.DbError is handled")
        tb = safe_log(traceback.format_exception(type(exc), exc, exc.__traceback__))
        logger.opt(exception=exc).error(
            f"Internal message: {exc.internal_message}, "
            f"Internal code: {exc.internal_code}, "
            f"HTTP response code: {exc.http_code}, "
            f"External message: {exc.external_message}, "
            f"Traceback: {tb}"
        )
        logger.critical(f"Response: {exc.external_message}")
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(BaseCustomError)
    async def custom_exception_handler(
        request: Request,
        exc: BaseCustomError,
    ):
        logger.critical("BaseCustomError is handled")
        tb = safe_log(traceback.format_exception(type(exc), exc, exc.__traceback__))
        logger.opt(exception=exc).error(
            f"Internal message: {exc.internal_message}, "
            f"Internal code: {exc.internal_code}, "
            f"HTTP response code: {exc.http_code}, "
            f"External message: {exc.external_message}, "
            f"Traceback: {tb}"
        )
        logger.critical(f"Response: {exc.external_message}")
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(Exception)
    async def custom_generic_handler(
        request: Request,
        exc: Exception,
    ):
        logger.opt(exception=exc).exception("Generic Exception is handled")
        tb = safe_log(traceback.format_exception(type(exc), exc, exc.__traceback__))
        logger.opt(exception=exc).critical(f"Unhandled Exception, Traceback is: {tb}")
        logger.critical(f"Response: Internal Server Error. Our team is notified.")
        return JSONResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error. Our team is notified."},
        )

    return app
