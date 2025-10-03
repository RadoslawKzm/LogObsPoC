import fastapi

from ._4000_base import DbError


# === 41xx SQL Errors =========================================================
class SQLError(DbError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4100
    internal_message = (
        "Base SQL exception. If visible in logs, something went uncaught."
    )


class ConnError(SQLError):  # Not Connection due to built-in conflict
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 4101
    internal_message = "Failed to establish a connection to the SQL database."


class IntegrityError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4102
    internal_message = "Integrity constraint violated (foreign key, unique)."


class DataError(SQLError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 4103
    internal_message = "Sent data is invalid or incompatible with schema."


class OperationalError(SQLError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 4104
    internal_message = "DB operation failed due to I/O or connection issue."


class ProgrammingError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4105
    internal_message = "SQL statement contains a programming or syntax error."


class InvalidRequestError(SQLError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 4106
    internal_message = "SQL operation was malformed or unsupported."


class DatabaseError(SQLError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4107
    internal_message = "Parent class of SQLAlchemy exceptions."


class AddRecordError(SQLError):
    http_code = fastapi.status.HTTP_409_CONFLICT
    internal_code = 4108
    internal_message = (
        "Unexpected add_record error occurred. "
        "Probably adding value to an unique colum that already exists."
    )
