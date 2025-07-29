import random

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend.api.v1.routers.health import response_examples

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get(
    "/",
    status_code=200,
    responses=response_examples.health,
)
async def health() -> dict:
    responses = [
        "I am Groot",
        "This is the way",
        "Luke, I am your father",
        "Hodor...",
    ]
    return {"data": random.choice(responses)}
