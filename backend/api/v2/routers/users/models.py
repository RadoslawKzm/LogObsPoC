import pydantic
from backend.api.v2.routers.models import Page


class User(pydantic.BaseModel):
    user_id: str
    name: str
    email: str
    model_config = {"from_attributes": True}  # <-- allow User instances


class UserUpdate(pydantic.BaseModel):
    name: str
    email: str


class UsersPageResponse(pydantic.BaseModel):
    users: list[User]
    page: Page
