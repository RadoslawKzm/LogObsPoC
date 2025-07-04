import fastapi
from loguru import logger

from backend.proj_exc import api_exceptions

api_exceptions_router = fastapi.APIRouter(
    prefix="/api-exceptions",
    tags=["api_exceptions"],
)


@api_exceptions_router.get("/", status_code=200)
async def example_get() -> fastapi.responses.JSONResponse:
    logger.info("get endpoint")
    return fastapi.responses.JSONResponse(
        content={"data": "Example response"},
        status_code=fastapi.status.HTTP_200_OK,
    )


@api_exceptions_router.get("/random-exception", status_code=200)
async def example_get_base_exception() -> fastapi.responses.JSONResponse:
    """This endpoint represents random, in code, uncaught exception.
    Shit happened that no one expected.
    """
    lst = [1, 2, 3, 4]
    return lst[20]


@api_exceptions_router.get("/{example_id}", status_code=200)
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
        raise api_exceptions.ResourceNotFoundException(
            internal_message=f"fGet example with id. "
            f"Request for {example_id=} not found"
        )
    return fastapi.responses.JSONResponse(
        content={"data": f"Example ID: {example_id} found."},
        status_code=fastapi.status.HTTP_200_OK,
    )
