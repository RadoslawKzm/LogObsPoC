import fastapi

from ._2000_base import DbError


# === 21xx SQL codes (HTTP 5xx) ===
class SQLError(DbError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Unexpected error. We're looking into it."
    internal_code = 2100
    internal_message = (
        "Base unexpected SQL exception. ",
        "If visible in logs, something went uncaught.",
    )

class ConnError(SQLError):  # Not Connection due to built-in conflict
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "Temporary issue. Please try again shortly."
    internal_code = 2101
    internal_message = "Failed to establish a connection to the SQL database."


class IntegrityError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "A data error occurred. Please contact support."
    internal_code = 2102
    internal_message = "Integrity constraint violated (foreign key, unique)."


class DataError(SQLError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Invalid data provided."
    internal_code = 2103
    internal_message = "Sent data is invalid or incompatible with schema."


class OperationalError(SQLError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "Temporary service issue. Try again later."
    internal_code = 2104
    internal_message = "DB operation failed due to I/O or connection issue."


class ProgrammingError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Something went wrong. Please try again later."
    internal_code = 2105
    internal_message = "SQL statement contains a programming or syntax error."


class InvalidRequestError(SQLError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "The request was invalid or unsupported."
    internal_code = 2106
    internal_message = "SQL operation was malformed or unsupported."


class DatabaseError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "An unexpected database error occurred."
    internal_code = 2107
    internal_message = "Parent class of SQLAlchemy exceptions."
