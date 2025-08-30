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

from .models import AllowedDbMethod

db_router = fastapi.APIRouter(prefix="/database", tags=["Database"])

"""Exposing databases CRUD operations as example."""


@db_router.get("/postgres/{method}", status_code=200)
async def postgres_endpoint(
    pg_db: typing.Annotated[
        "PostgresImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Postgres")),
    ],
    method: AllowedDbMethod,
):
    try:
        return await getattr(pg_db, method)()
    except TypeError:
        return await getattr(pg_db, method)("Test")


@db_router.get("/mongo/{method}", status_code=200)
async def mongo_endpoint(
    mongo_db: typing.Annotated[
        "MongoImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mongo")),
    ],
    method: AllowedDbMethod,
):
    try:
        return await getattr(mongo_db, method)()
    except TypeError:
        return await getattr(mongo_db, method)("Test")


@db_router.get("/mock/record/{record_id}", status_code=200)
async def mock_endpoint_1(
    mock_db: typing.Annotated[
        "MockImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mock")),
    ],
    record_id: int,
) -> dict:
    return await mock_db.get_record(record_id=record_id)


@db_router.get("/mock/many_record/", status_code=200)
async def mock_endpoint_2(
    mock_db: typing.Annotated[
        "MockImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mock")),
    ],
) -> list:
    return await mock_db.get_many_records()


@db_router.delete("/mock/record/{record_id}", status_code=204)
async def mock_endpoint_3(
    mock_db: typing.Annotated[
        "MockImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mock")),
    ],
    record_id: int,
):
    await mock_db.delete_record(record_id=record_id)


@db_router.delete("/mock/many_records", status_code=204)
async def mock_endpoint_4(
    mock_db: typing.Annotated[
        "MockImplementation",
        Depends(DatabaseInterface.get_db_impl(db_name="Mock")),
    ],
):
    await mock_db.delete_many_records()
