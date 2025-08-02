import fastapi
from loguru import logger

from ...exceptions import (
    api_exceptions,
    auth_exceptions,
    core_exceptions,
    db_exceptions,
)

exceptions_router = fastapi.APIRouter(
    prefix="/exceptions",
    tags=["exceptions"],
)


@exceptions_router.get("/", status_code=200)
async def example_get() -> fastapi.responses.JSONResponse:
    logger.info("get endpoint")
    return fastapi.responses.JSONResponse(
        content={"data": "Example response"},
        status_code=fastapi.status.HTTP_200_OK,
    )


@exceptions_router.get("/example_get_id/{example_id}", status_code=200)
async def example_get_id_not_found(
    example_id: int,
) -> fastapi.responses.JSONResponse:
    """
    This endpoint will give simulated not found exception.
    ID's in database {1,2,3,4,5,6,7,8,9}.
    If you want to trigger exception choose something else.

    :param example_id:
    :return:
    """
    database = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    if example_id not in database:
        raise api_exceptions.ResourceNotFoundError(
            internal_message=f"fGet example with id. "
            f"Request for {example_id=} not found"
        )
    return fastapi.responses.JSONResponse(
        content={"data": f"Example ID: {example_id} found."},
        status_code=fastapi.status.HTTP_200_OK,
    )


@exceptions_router.get("/generic-exception")
async def example_get_generic_exception() -> fastapi.responses.JSONResponse:
    """This endpoint represents random, in code, uncaught exception.
    Shit happened that no one expected.
    """
    lst = [1, 2, 3, 4]
    return lst[20]


####### ---------- API Exceptions ---------- #######
@exceptions_router.get("/api-exception")
async def example_get_api_exception(
    resource_name: str = fastapi.Query(
        default="test",
        min_length=1,
        max_length=10,
    )
) -> fastapi.responses.JSONResponse:
    """This endpoint represents manually invoked api exception.
    This is meant to represent flow control in endpoints.
    """
    raise api_exceptions.ResourceNotFoundError(
        external_message=f"Requested resource: {resource_name} Not Found!"
    )


####### ---------- Auth Exceptions ---------- #######
@exceptions_router.get("/auth-exception")
async def example_get_auth_exception(
    role: str = fastapi.Query(
        default="test",
        min_length=1,
        max_length=10,
    )
) -> fastapi.responses.JSONResponse:
    """This endpoint represents manually invoked api exception.
    This is meant to represent flow control in endpoints.
    """
    raise auth_exceptions.AuthorizationError(
        external_message=f"Requested role: {role} Not authenticated!"
    )


####### ---------- Core Exceptions ---------- #######
@exceptions_router.get("/core-exception")
async def example_get_core_exception(
    service: str = fastapi.Query(
        default="test",
        min_length=1,
        max_length=10,
    )
) -> fastapi.responses.JSONResponse:
    """This endpoint represents manually invoked api exception.
    This is meant to represent flow control in endpoints.
    """
    raise core_exceptions.ExternalServiceError(
        external_message=f"Requested service: {service} Not available!"
    )


####### ---------- DB Exceptions ---------- #######
@exceptions_router.get("/db-exception")
async def example_get_db_exception(
    record_name: str = fastapi.Query(
        default="test",
        min_length=1,
        max_length=10,
    )
) -> fastapi.responses.JSONResponse:
    """This endpoint represents manually invoked api exception.
    This is meant to represent flow control in endpoints.
    """
    raise db_exceptions.RecordNotFoundError(
        external_message=f"Requested record: {record_name} Not Found!"
    )
