from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend.api.v1.routers.about import response_examples

about_router = APIRouter(prefix="/about", tags=["about"])


@about_router.get("/", status_code=200, responses=response_examples.about)
def about() -> JSONResponse:
    return JSONResponse(
        content={"data": "version_v2"},
        status_code=status.HTTP_200_OK,
    )
