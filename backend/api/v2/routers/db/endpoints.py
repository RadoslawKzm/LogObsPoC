import typing

import fastapi
from fastapi import Depends

from backend.database import DatabaseInterface

if typing.TYPE_CHECKING:
    from backend.database import (
        MockImplementation,
        MongoImplementation,
        PostgresImplementation,
    )


db_router = fastapi.APIRouter(prefix="/database", tags=["Database"])


@db_router.get("/postgres", status_code=200)
async def postgres_endpoint(
    pg_db: typing.Annotated[
        "PostgresImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Postgres")),
    ],
):
    return await pg_db.get_record()


@db_router.get("/mongo", status_code=200)
async def mongo_endpoint(
    mongo_db: typing.Annotated[
        "MongoImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mongo")),
    ],
):
    return await mongo_db.get_many_records()


@db_router.get("/mock", status_code=200)
async def mock_endpoint(
    mock_db: typing.Annotated[
        "MockImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mock")),
    ],
):
    return await mock_db.get_many_records()
