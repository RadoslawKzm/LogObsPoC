import fastapi
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from loguru import logger
import typing

from . import response_examples
from backend.database import DatabaseInterface

files_router = fastapi.APIRouter(prefix="/files", tags=["files"])

if typing.TYPE_CHECKING:
    from backend.database import (
        MockImplementation,
        MongoImplementation,
        PostgresImplementation,
        FileStorageImplementation,
    )


@files_router.get(
    "/",
    status_code=200,
    # responses=response_examples.response_200,
)
async def get_files(
    file_storage: typing.Annotated[
        "FileStorageImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="FileStorage")),
    ],
) -> fastapi.responses.ORJSONResponse:
    return ORJSONResponse(await file_storage.list_records())
