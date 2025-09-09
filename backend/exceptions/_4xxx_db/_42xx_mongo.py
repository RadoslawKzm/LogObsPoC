import fastapi

from ._4000_base import DbError


# === 42xx SQL codes (HTTP 5xx) ===
class MongoError(DbError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4200
    internal_message = (
        "Base unexpected MongoDB exception. ",
        "If visible in logs, something went uncaught.",
    )

class ExampleError(MongoError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4201
    internal_message = (
        "Base unexpected MongoDB exception. ",
        "If visible in logs, something went uncaught.",
    )