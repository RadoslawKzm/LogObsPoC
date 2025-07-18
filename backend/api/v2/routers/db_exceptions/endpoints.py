import fastapi
import sqlalchemy
import sqlalchemy.exc

from backend.api.v2.exc import db_exceptions

db_exceptions_router = fastapi.APIRouter(
    prefix="/database-exceptions",
    tags=["db_exceptions"],
)


@db_exceptions_router.get("/", status_code=200)
async def database_exception_endpoint() -> fastapi.responses.JSONResponse:
    """Showing random exception is propagated outside of session manager."""
    x = 1 / 0  # noqa: F841
    return fastapi.responses.JSONResponse(
        content={"data": "Example response"},
        status_code=fastapi.status.HTTP_200_OK,
    )


@db_exceptions_router.get("/db-exception/_id", status_code=200)
async def developer_risen_exception_endpoint(
    _id: int,
) -> fastapi.responses.JSONResponse:
    """Scenario when developer is looking for ID in db in CORE module.
       ID is not found and dev is rising manual db exception to control flow.
       Dev is rising DB exception Not found giving HTTP404

    :param int _id:
    :param AsyncSession session:
    :return:
    """
    raise db_exceptions.RecordNotFoundError(
        f"Could not find ID={_id} in the database"
    )


@db_exceptions_router.get("/db-exception", status_code=200)
async def database_error_endpoint(
) -> fastapi.responses.JSONResponse:
    """Scenario when something unexpected happens with database.
    We are getting some random SQLAlchemy exception.
    PostgresSessionManager is rising DB exception from HTTP5xx series.

    :param session:
    :return:
    """
    raise sqlalchemy.exc.OperationalError(
        statement="SELECT * FROM some_table",
        params={},
        orig=Exception("Manual DatabaseError"),
    )
