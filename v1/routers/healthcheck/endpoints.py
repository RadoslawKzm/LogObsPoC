import random

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend.api.v1.routers.healthcheck import response_examples

healthcheck_router = APIRouter(prefix="/health", tags=["health"])


@healthcheck_router.get("/", status_code=200, responses=response_examples.health)
async def health() -> JSONResponse:
    responses = ["I am Groot", "This is the way", "Luke, I am your father", "Hodor..."]
    return JSONResponse(
        content={"data": random.choice(responses)},
        status_code=status.HTTP_200_OK,
    )
