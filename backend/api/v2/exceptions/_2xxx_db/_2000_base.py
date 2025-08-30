import fastapi

from backend.api.v2.exceptions._0_500_base import BaseCustomError


class DbError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Internal Server Error. Our team is notified."
    internal_code = 2000
    internal_message = (
        "Base unexpected generic DB exception. ",
        "If visible in logs, something went uncaught.",
    )