import fastapi

from . import get_user


class APIRouter(fastapi.APIRouter):
    """
    Extension of FastAPI's APIRouter for specific dependency inclusion.

    This class customizes FastAPI's APIRouter by automatically including
    a dependency to ensure the user is retrieved for each route. It is useful
    for applications that require consistent user context across all endpoints.

    Attributes:
        dependencies (list): List of dependencies to be applied to all routes
            of this router, including the `get_user` dependency to fetch the
            current user context.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            dependencies=[fastapi.Depends(get_user)],
            **kwargs,
        )
