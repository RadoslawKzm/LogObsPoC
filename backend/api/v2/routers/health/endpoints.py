import random

from backend import auth

from . import examples

health_router = auth.APIRouter(prefix="/health", tags=["Health"])


@health_router.get(
    "/",
    status_code=200,
    responses=examples.response.success,
)
async def health() -> dict:
    responses = [
        "I am Groot",
        "This is the way",
        "Luke, I am your father",
        "Hodor...",
    ]
    return {"data": random.choice(responses)}
