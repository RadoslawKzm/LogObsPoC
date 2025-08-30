import fastapi

from ._2000_base import DbError


# === 21xx SQL codes (HTTP 5xx) ===
class MongoError(DbError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Unexpected error. We're looking into it."
    internal_code = 2200
    internal_message = (
        "Base unexpected MongoDB exception. ",
        "If visible in logs, something went uncaught.",
    )