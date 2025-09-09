import fastapi

from .._0_500_base import BaseCustomError


class DbError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4000
    internal_message = (
        "Base unexpected generic DB exception. ",
        "If visible in logs, something went uncaught.",
    )
