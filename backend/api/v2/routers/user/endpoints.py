import typing

import fastapi
from backend.database import DatabaseInterface
from backend.exceptions import api_exceptions
from . import examples

from . import User

if typing.TYPE_CHECKING:
    from backend.database import PostgresImplementation


user_router = fastapi.APIRouter(prefix="/user", tags=["User"])
PG_SESSION = typing.Annotated[
    "PostgresImplementation",
    fastapi.Depends(DatabaseInterface.get_db_impl(db_name="Postgres")),
]
# Example users
user_examples = {
    "alice": {
        "summary": "Example Alice",
        "description": "A sample user with an email from example.com",
        "value": {"user_id": "user_1", "name": "Alice Doe", "email": "alice@example.com"},
    },
    "bob": {
        "summary": "Example Bob",
        "description": "Another sample user, Gmail address",
        "value": {"user_id": "user_2", "name": "Bob Smith", "email": "bob@gmail.com"},
    },
    "carol": {
        "summary": "Example Carol",
        "description": "Third user with company domain email",
        "value": {"user_id": "user_3", "name": "Carol Johnson", "email": "carol@company.org"},
    },
}

@user_router.get(
    "/{user_id}",
    status_code=fastapi.status.HTTP_200_OK,
    responses=examples.response.tst
    # responses={
    #     200: {
    #         "description": "User found and returned",
    #         "content": {
    #             "application/json": {
    #                 "examples": user_examples
    #             }
    #         },
    #     },
    #     404: {"description": "User not found"},
    #     500: {"description": "Internal server error"},
    # },
)
async def get_user(
    pg_db: PG_SESSION,
    user_id: str = fastapi.Path(..., example="user_1"),
) -> User:
    result: User = await pg_db.get_record(
        key="user_id",
        value=user_id,
        place="users",
    )
    if not result:
        raise api_exceptions.NotFoundError(f"User: {user_id} not found")
    return await pg_db.get_record(
        key="user_id",
        value=user_id,
        place="users",
    )


@user_router.put("/{user_id}", status_code=fastapi.status.HTTP_200_OK)
async def update_user(
    user: User,
    pg_db: PG_SESSION,
    user_id: str = fastapi.Path(..., example="user_1"),
) -> User:
    existing_user = await pg_db.get_record(
        key="user_id",
        value=user_id,
        place="users",
    )
    if not existing_user:
        raise api_exceptions.NotFoundError(f"User: {user_id} not found")
    updated_user = await pg_db.update_record(
        place="users",
        key="user_id",
        value=user_id,
        record=user.model_dump(),
    )
    return updated_user


@user_router.delete(
    "/{user_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    pg_db: PG_SESSION,
    user_id: str = fastapi.Path(..., example="user_1"),
):
    existing_user = await pg_db.get_record(
        key="user_id",
        value=user_id,
        place="users",
    )
    if not existing_user:
        raise api_exceptions.NotFoundError(f"User: {user_id} not found")
    await pg_db.delete_record(
        place="users",
        key="user_id",
        value=user_id,
    )
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@user_router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_user(
    pg_db: PG_SESSION,
    user: User = fastapi.Body(
        ...,
        openapi_examples=examples.request.users,
    ),
) -> User:
    new_user: User = await pg_db.add_record(
        place="users",
        record=user,
    )
    return new_user
