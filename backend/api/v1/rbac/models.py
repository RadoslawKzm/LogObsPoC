from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class User(BaseModel):
    id: int
    username: str
    role: Role
