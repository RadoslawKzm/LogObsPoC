import fastapi
from loguru import logger

from . import response_examples

about_router = fastapi.APIRouter(prefix="/about", tags=["about"])


@about_router.get(
    "/",
    status_code=200,
    responses=response_examples.response_200,
)
async def about() -> fastapi.responses.JSONResponse:
    logger.debug("About is called")
    return fastapi.responses.JSONResponse(
        content={"data": "version_v2"},
        status_code=fastapi.status.HTTP_200_OK,
    )
