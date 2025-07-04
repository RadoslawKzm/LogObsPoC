import random

import fastapi

from . import response_examples

healthcheck_router = fastapi.APIRouter(prefix="/health", tags=["health"])


@healthcheck_router.get(
    "/",
    status_code=200,
    responses=response_examples.response_200,
)
async def health() -> fastapi.responses.JSONResponse:
    responses = [
        "I am Groot",
        "This is the way",
        "Luke, I am your father",
        "Hodor...",
    ]
    return fastapi.responses.JSONResponse(
        content={"data": random.choice(responses)},
        status_code=fastapi.status.HTTP_200_OK,
    )
