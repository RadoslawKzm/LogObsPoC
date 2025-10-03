import typing

import fastapi

from backend.database import PG_SESSION
from backend.exceptions import api_exceptions

from . import (
    Page,
    Workspace,
    WorkspacesPageResponse,
    WorkspaceUpdate,
)

workspaces_router = fastapi.APIRouter(
    prefix="/workspaces", tags=["Workspaces"]
)
if typing.TYPE_CHECKING:
    from backend.database import PostgresImplementation


@workspaces_router.get(
    "/{workspace_id}",
    status_code=fastapi.status.HTTP_200_OK,
    # responses=examples.response.workspaces_get_workspace,
)
async def get_workspace(
    pg_db: "PostgresImplementation" = PG_SESSION,
    workspace_id: str = fastapi.Path(..., example="1"),
) -> Workspace:
    result: Workspace = await pg_db.get_record(
        key="workspace_id",
        value=workspace_id,
        place="workspaces",
    )
    if not result:
        raise api_exceptions.NotFoundError(
            f"Workspace: {workspace_id} not found"
        )
    return result


@workspaces_router.get(
    "/",
    status_code=fastapi.status.HTTP_200_OK,
    # responses=examples.response.workspaces_get_many_workspaces,
)
async def get_many_workspaces(
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
) -> WorkspacesPageResponse:
    """
    Fetch paginated list of workspaces.
    """
    workspaces: list[Workspace] = await pg_db.get_many_records(
        page_num=page_num,
        page_size=page_size,
        place="workspaces",
    )
    # if not workspaces:
    #     raise api_exceptions.NotFoundError("No workspaces found")

    next_page = None
    if len(workspaces) == page_size + 1:
        # Check if next page is available.
        # `get_many_records` returns page_size + 1
        base_url = str(request.url_for("get_many_workspaces"))
        next_page = f"{base_url}?page={page_num+1}&page_size={page_size}"
        workspaces = workspaces[:-1]

    page: Page = Page(
        page_num=page_num,
        page_size=page_size,
        total_items=len(workspaces),
        next_page=next_page,
    )
    return WorkspacesPageResponse(workspaces=workspaces, page=page)


@workspaces_router.patch(
    "/{workspace_id}", status_code=fastapi.status.HTTP_200_OK
)
async def update_workspace(
    pg_db: "PostgresImplementation" = PG_SESSION,
    workspace_id: str = fastapi.Path(..., example="workspace_1"),
    workspace: WorkspaceUpdate = fastapi.Body(...),  # noqa: B008
) -> Workspace:
    existing_workspace: Workspace = await pg_db.get_record(
        key="workspace_id",
        value=workspace_id,
        place="workspaces",
    )
    if not existing_workspace:
        raise api_exceptions.NotFoundError(
            f"Workspace: {workspace_id} not found"
        )
    existing_workspace.name = workspace.name
    existing_workspace.email = workspace.email
    updated_workspace = await pg_db.update_record(
        data=existing_workspace,
        place="workspaces",
    )
    return updated_workspace


@workspaces_router.delete(
    "/{workspace_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
    # responses=examples.response.workspaces_delete_workspace,
)
async def delete_workspace(
    pg_db: "PostgresImplementation" = PG_SESSION,
    workspace_id: str = fastapi.Path(..., example="workspace_1"),
):
    result = await pg_db.delete_record(
        key="workspace_id",
        value=workspace_id,
        place="workspaces",
    )
    if result == 0:
        raise api_exceptions.NotFoundError(
            f"Workspace: {workspace_id} not found"
        )
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@workspaces_router.post(
    "/",
    status_code=fastapi.status.HTTP_201_CREATED,
    # responses=examples.response.workspaces_create_workspace,
)
async def create_workspace(
    pg_db: "PostgresImplementation" = PG_SESSION,
    workspace: Workspace = fastapi.Body(...),  # noqa: B008
) -> Workspace:
    new_workspace: Workspace = await pg_db.add_record(
        place="workspaces",
        record=workspace,
    )
    return new_workspace
