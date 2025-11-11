import fastapi
from loguru import logger

from backend import auth

from . import examples

about_router = auth.APIRouter(
    prefix="/about",
    tags=["About"],
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


data = {
    "DocumentID": "123",
    "UDIF": "abc",
    "Properties": [
        {"Name": "opt1", "Value": "val1"},
        {"Name": "opt2", "Value": "ignore me"},
        {"Name": "opt3", "Value": "val3"}
    ],
}
