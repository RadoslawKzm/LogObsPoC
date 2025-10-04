import fastapi
from loguru import logger

from backend.api.auth import get_current_user

from . import examples

about_router = fastapi.APIRouter(
    prefix="/about",
    tags=["About"],
    dependencies=[fastapi.Depends(get_current_user)],
)


@about_router.get(
    "/",
    status_code=200,
    responses=examples.response.success,
)
async def about() -> fastapi.responses.JSONResponse:
    logger.debug("About is called")
    return fastapi.responses.JSONResponse(
        content={"data": "version_v2"},
        status_code=fastapi.status.HTTP_200_OK,
    )
