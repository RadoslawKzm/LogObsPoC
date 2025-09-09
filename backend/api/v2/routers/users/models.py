import pydantic
from backend.api.v2.routers.models import Page


class User(pydantic.BaseModel):
    user_id: str
    name: str
    email: str
    model_config = {"from_attributes": True}  # <-- allow User instances


class UserPageResponse(pydantic.BaseModel):
    users: list[User]
    page: Page
