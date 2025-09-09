import pydantic
from backend.api.v2.routers.models import Page


class Workspace(pydantic.BaseModel):
    workspace_id: str
    name: str
    user_id: str
    model_config = {"from_attributes": True}  # <-- allow Workspace instances


class WorkspaceUpdate(pydantic.BaseModel):
    name: str
    user_id: str


class WorkspacesPageResponse(pydantic.BaseModel):
    workspaces: list[Workspace]
    page: Page
