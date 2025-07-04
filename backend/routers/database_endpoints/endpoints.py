import typing
import fastapi
from fastapi import Depends

from backend.database.interface import DatabaseInterface


db_router = fastapi.APIRouter(
    prefix="/database",
    tags=["Database"],
)


@db_router.get("/postgres", status_code=200)
async def postgres_endpoint(
    pg_db: typing.Annotated[
        DatabaseInterface,
        Depends(DatabaseInterface.get_db_impl(db_name="Postgres")),
    ],
    # mongo_db=Depends(DatabaseInterface.get_db_impl(db_name="Mongo")),
):
    """Showing random exception is propagated outside of session manager."""
    await pg_db.get_record()


@db_router.get("/mongo", status_code=200)
async def mongo_endpoint(
    mongo_db: typing.Annotated[
        DatabaseInterface,
        Depends(DatabaseInterface.get_db_impl(db_name="Mongo")),
    ],
):
    """Showing random exception is propagated outside of session manager."""
    await mongo_db.get_many_records()
