import pydantic


class User(pydantic.BaseModel):
    user_id: str
    name: str
    email: str
