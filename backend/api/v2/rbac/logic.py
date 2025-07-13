from fastapi import Depends

from backend.api.v2.exc import api_exceptions
from backend.api.v2.rbac.models import Role, User


def get_current_user() -> User:
    # Replace with real auth logic (JWT, session, etc.)
    return User(id=1, username="johndoe", role=Role.ADMIN)


def require_role(*allowed_roles: Role):
    def role_checker(user=Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise api_exceptions.ForbiddenException()
        return user  # pass user to endpoint

    return role_checker
