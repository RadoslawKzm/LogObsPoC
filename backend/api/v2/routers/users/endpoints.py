import typing

import fastapi

from backend.database import PG_SESSION
from backend.exceptions import api_exceptions

from . import Page, User, UsersPageResponse, UserUpdate, examples

users_router = fastapi.APIRouter(prefix="/users", tags=["Users"])

if typing.TYPE_CHECKING:
    from backend.database import PostgresImplementation


@users_router.get(
    "/{user_id}",
    status_code=fastapi.status.HTTP_200_OK,
    responses=examples.response.users_get_user,
)
async def get_user(
    pg_db: "PostgresImplementation" = PG_SESSION,
    user_id: str = fastapi.Path(..., example="user_1"),
) -> User:
    result: User = await pg_db.get_record(
        key="user_id",
        value=user_id,
        place="users",
    )
    if not result:
        raise api_exceptions.NotFoundError(f"User: {user_id} not found")
    return result


@users_router.get(
    "/",
    status_code=fastapi.status.HTTP_200_OK,
    responses=examples.response.users_get_many_users,
)
async def get_many_users(
    pg_db: "PostgresImplementation" = PG_SESSION,
    page_num: int = fastapi.Query(
        1,
        ge=1,
        description="Page number (starting from 1)",
    ),
    page_size: int = fastapi.Query(
        20,
        ge=1,
        le=100,
        description="Number of results per page_num",
    ),
    request: fastapi.Request = None,
) -> UsersPageResponse:
    """
    Fetch a paginated list of users.
    """
    users: list[User] = await pg_db.get_many_records(
        page_num=page_num,
        page_size=page_size,
        place="users",
    )
    next_page = None
    if len(users) == page_size + 1:
        # Check if next page is available.
        # `get_many_records` returns page_size + 1
        base_url = str(request.url_for("get_many_users"))
        next_page = f"{base_url}?page={page_num+1}&page_size={page_size}"
        users = users[:-1]
    page: Page = Page(
        page_num=page_num,
        page_size=page_size,
        total_items=len(users),
        next_page=next_page,
    )
    return UsersPageResponse(users=users, page=page)


@users_router.patch("/{user_id}", status_code=fastapi.status.HTTP_200_OK)
async def update_user(
    pg_db: "PostgresImplementation" = PG_SESSION,
    user_id: str = fastapi.Path(..., example="user_1"),
    user: UserUpdate = fastapi.Body(  # noqa: B008
        ...,
        openapi_examples=examples.request.users,
    ),
) -> User:
    existing_user: User = await pg_db.get_record(
        key="user_id",
        value=user_id,
        place="users",
    )
    if not existing_user:
        raise api_exceptions.NotFoundError(f"User: {user_id} not found")
    existing_user.name = user.name
    existing_user.email = user.email
    updated_user = await pg_db.update_record(
        data=existing_user,
        place="users",
    )
    return updated_user


@users_router.delete(
    "/{user_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
    responses=examples.response.users_delete_user,
)
async def delete_user(
    pg_db: "PostgresImplementation" = PG_SESSION,
    user_id: str = fastapi.Path(..., example="user_1"),
):
    result = await pg_db.delete_record(
        key="user_id",
        value=user_id,
        place="users",
    )
    if result == 0:
        raise api_exceptions.NotFoundError(f"User: {user_id} not found")
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@users_router.post(
    "/",
    status_code=fastapi.status.HTTP_201_CREATED,
    responses=examples.response.users_create_user,
)
async def create_user(
    pg_db: "PostgresImplementation" = PG_SESSION,
    user: User = fastapi.Body(  # noqa: B008
        ...,
        openapi_examples=examples.request.users,
    ),
) -> User:
    new_user: User = await pg_db.add_record(
        place="users",
        record=user,
    )
    return new_user
