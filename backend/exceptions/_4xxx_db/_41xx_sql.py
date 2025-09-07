import fastapi

from ._4000_base import DbError


# === 41xx SQL Errors (HTTP 5xx) ===============================================
class SQLError(DbError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4100
    external_message = "Unexpected error. We're looking into it."
    internal_message = (
        "Base SQL exception. If visible in logs, something went uncaught."
    )


class ConnError(SQLError):  # Not Connection due to built-in conflict
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 4101
    external_message = "Temporary issue. Please try again shortly."
    internal_message = "Failed to establish a connection to the SQL database."


class IntegrityError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4102
    external_message = "A data error occurred. Please contact support."
    internal_message = "Integrity constraint violated (foreign key, unique)."


class DataError(SQLError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 4103
    external_message = "Invalid data provided."
    internal_message = "Sent data is invalid or incompatible with schema."


class OperationalError(SQLError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 4104
    external_message = "Temporary service issue. Try again later."
    internal_message = "DB operation failed due to I/O or connection issue."


class ProgrammingError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4105
    external_message = "Something went wrong. Please try again later."
    internal_message = "SQL statement contains a programming or syntax error."


class InvalidRequestError(SQLError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 4106
    external_message = "The request was invalid or unsupported."
    internal_message = "SQL operation was malformed or unsupported."


class DatabaseError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4107
    external_message = "An unexpected database error occurred."
    internal_message = "Parent class of SQLAlchemy exceptions."
