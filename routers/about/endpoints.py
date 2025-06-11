import fastapi

from . import response_examples

about_router = fastapi.APIRouter(prefix="/info", tags=["about"])


@about_router.get(
    "/",
    status_code=200,
    responses=response_examples.response_200,
)
def about() -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        content={"data": "version_v1"},
        status_code=fastapi.status.HTTP_200_OK,
    )
