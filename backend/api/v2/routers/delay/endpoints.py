import asyncio

import fastapi
from loguru import logger

from backend.api.loguru_logger import TimingContextManager

delay_router = fastapi.APIRouter(
    prefix="/delay",
    tags=["delay"],
)


@delay_router.get("/", status_code=200)
async def example_get() -> fastapi.responses.JSONResponse:
    async with TimingContextManager(name="Timing delay example"):
        logger.info("Delay 5s")
        await asyncio.sleep(5)
    return fastapi.responses.JSONResponse(
        content={"data": "Example response"},
        status_code=fastapi.status.HTTP_200_OK,
    )
