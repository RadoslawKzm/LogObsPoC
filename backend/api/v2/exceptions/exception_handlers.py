import traceback
import typing

from fastapi import HTTPException, status, FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from loguru import logger

if typing.TYPE_CHECKING:
    from loguru import Logger

from backend.loguru_logger import safe_log

from .api import ApiError
from .db import DbError
from .base import BaseCustomError
from .core import CoreError
from .auth import AuthError
from .cloud import CloudError


def log_traceback(
    *,
    logger_obj: "Logger",
    level: str,
    exc: BaseCustomError,
) -> None:
    logger_obj.log(level, f"{type(exc)} is handled.")
    logger_obj.opt(exception=exc).log(
        level,
        f"Internal message: {exc.internal_message}, "
        f"Internal code: {exc.internal_code}, "
        f"HTTP response code: {exc.http_code}, "
        f"External message: {exc.external_message}, "
        f"Traceback: {safe_log(''.join(traceback.format_exc()))}",
    )
    logger_obj.log(level, f"Response: {exc.external_message}")


def add_exception_handlers(app: FastAPI) -> FastAPI:
    @app.exception_handler(ApiError)
    async def manual_http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        logger.info("Manual in-code exception was risen.")
        logger.info(f"Status code: {exc.status_code}")
        logger.info(f"Detail: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        logger.log("HTTPExc", "Manual in-code exception was risen.")
        logger.log("HTTPExc", f"Status code: {exc.status_code}")
        logger.log("HTTPExc", f"Detail: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(ApiError)
    async def api_exception_handler(
        request: Request,
        exc: ApiError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="HTTPExc", exc=exc)
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(AuthError)
    async def api_exception_handler(
        request: Request,
        exc: AuthError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="HTTPExc", exc=exc)
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(CoreError)
    async def api_exception_handler(
        request: Request,
        exc: CoreError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="ERROR", exc=exc)
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(CloudError)
    async def api_exception_handler(
        request: Request,
        exc: CloudError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="ERROR", exc=exc)
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(DbError)
    async def db_exception_handler(
        request: Request,
        exc: DbError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="ERROR", exc=exc)
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(BaseCustomError)
    async def custom_exception_handler(
        request: Request,
        exc: BaseCustomError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="CRITICAL", exc=exc)
        return JSONResponse(
            status_code=exc.http_code,
            content={"message": exc.external_message},
        )

    @app.exception_handler(Exception)
    async def custom_generic_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.opt(exception=exc).critical("Generic Exception is handled")
        logger.exception("Unhandled Exception")
        msg: str = "Internal Server Error. Our team is notified."
        logger.critical(f"Response: {msg}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": msg},
        )

    return app
