import fastapi

from proj_exc.base import BaseCustomException


class DbException(BaseCustomException):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Something went wrong. Please try again later."
    internal_code = 21000
    internal_message = "Unexpected SQL error. This should not happen."


# === 211xx Manual SQL codes (HTTP 4xx) ===
class ManualDbException(DbException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "The request could not be completed."
    internal_code = 21100
    internal_message = (
        "Base developer risen exception. "
        "If visible in logs, something went wrong."
    )


class RecordNotFoundException(ManualDbException):
    http_code = fastapi.status.HTTP_404_NOT_FOUND
    external_message = "The requested resource was not found."
    internal_code = 21101
    internal_message = "No matching record found in the SQL database."


class ConnectionException(DbException):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "Temporary issue. Please try again shortly."
    internal_code = 21102
    internal_message = "Failed to establish a connection to the SQL database."


class ResourceExistsException(DbException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "The resource already exists."
    internal_code = 21103
    internal_message = "Attempted to create a resource that already exists."


class ResourceUpdateFailedException(DbException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Unable to update the resource."
    internal_code = 21104
    internal_message = (
        "Failed to update resource due to invalid or conflicting data."
    )


class DeletionFailedException(DbException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Unable to delete the item."
    internal_code = 21105
    internal_message = (
        "Deletion failed due to constraints or non-empty references."
    )


class RecordUpdateExistsException(DbException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Conflict occurred while updating the data."
    internal_code = 21106
    internal_message = "Updated record violates a uniqueness constraint."


class RequestedDeleteNotFoundException(DbException):
    http_code = fastapi.status.HTTP_404_NOT_FOUND
    external_message = "Nothing to delete at the specified location."
    internal_code = 21107
    internal_message = "Attempted to delete a non-existent record."


# === 212xx Unexpected SQL codes (HTTP 5xx) ===
class UnexpectedException(DbException):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Unexpected error. We're looking into it."
    internal_code = 21200
    internal_message = (
        "Base unexpected DB exception. "
        "If visible in logs, something went uncaught."
    )


class IntegrityException(UnexpectedException):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "A data error occurred. Please contact support."
    internal_code = 21201
    internal_message = (
        "Integrity constraint violated (e.g., foreign key, uniqueness)."
    )


class DataException(UnexpectedException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Invalid data provided."
    internal_code = 21202
    internal_message = "Sent data is invalid or incompatible with schema."


class OperationalException(UnexpectedException):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "Temporary service issue. Try again later."
    internal_code = 21203
    internal_message = (
        "Database operation failed due to I/O or connection issue."
    )


class ProgrammingException(UnexpectedException):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Something went wrong. Please try again later."
    internal_code = 21204
    internal_message = "SQL statement contains a programming or syntax error."


class InvalidRequestException(UnexpectedException):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "The request was invalid or unsupported."
    internal_code = 21205
    internal_message = "SQL operation was malformed or unsupported."


class DatabaseException(UnexpectedException):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "An unexpected database error occurred."
    internal_code = 21206
    internal_message = "Parent class of SQLAlchemy exceptions."
