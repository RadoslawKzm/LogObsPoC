import traceback
import typing

from fastapi import FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, ORJSONResponse
from loguru import logger

from . import BaseCustomError
from ._1xxx_auth import AuthError
from ._2xxx_api import ApiError
from ._3xxx_core import CoreError
from ._4xxx_db import DbError
from ._5xxx_cloud import CloudError

if typing.TYPE_CHECKING:
    from loguru import Logger


def log_traceback(
    *,
    logger_obj: "Logger",
    level: str,
    exc: BaseCustomError,
    tb: bool = True,
) -> None:
    logger_obj.log(level, f"{type(exc)} is handled.")
    logger_obj.opt(exception=exc).log(
        level,
        f"Internal message: {exc.internal_message}, "
        f"Internal code: {exc.internal_code}, "
        f"HTTP response code: {exc.http_code}, "
        f"External message: {exc.external_message}, ",
    )
    if tb:
        logger_obj.opt(exception=exc).log(
            level,
            f"Traceback: {''.join(traceback.format_exc())}",
        )
    logger_obj.log(level, f"Response: {exc.external_message}")


def prepare_orjson(exc: BaseCustomError, request: Request) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.http_code,
        content={
            "message": exc.external_message,
            "internal_code": exc.internal_code,
        },
    )


def add_exception_handlers(app: FastAPI) -> FastAPI:
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
    ) -> ORJSONResponse:
        log_traceback(logger_obj=logger, level="INFO", exc=exc, tb=False)
        return prepare_orjson(exc=exc, request=request)

    @app.exception_handler(AuthError)
    async def auth_exception_handler(
        request: Request,
        exc: AuthError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="WARNING", exc=exc)
        return prepare_orjson(exc=exc, request=request)

    @app.exception_handler(CoreError)
    async def core_exception_handler(
        request: Request,
        exc: CoreError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="ERROR", exc=exc)
        return prepare_orjson(exc=exc, request=request)

    @app.exception_handler(CloudError)
    async def cloud_exception_handler(
        request: Request,
        exc: CloudError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="ERROR", exc=exc)
        return prepare_orjson(exc=exc, request=request)

    @app.exception_handler(DbError)
    async def db_exception_handler(
        request: Request,
        exc: DbError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="ERROR", exc=exc)
        return prepare_orjson(exc=exc, request=request)

    @app.exception_handler(BaseCustomError)
    async def custom_exception_handler(
        request: Request,
        exc: BaseCustomError,
    ) -> JSONResponse:
        log_traceback(logger_obj=logger, level="CRITICAL", exc=exc)
        return prepare_orjson(exc=exc, request=request)

    @app.exception_handler(Exception)
    async def custom_generic_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.critical("Generic Exception is handled")
        formatted_exc = "".join(traceback.format_exc())
        logger.opt(exception=exc).critical(f"Traceback: {formatted_exc}")
        logger.critical(f"Response: {BaseCustomError.external_message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": BaseCustomError.external_message,
                "internal_code": BaseCustomError.internal_code,
            },
        )

    return app
