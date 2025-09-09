import fastapi
from ._4000_base import DbError


# === 43xx FileStorage Errors (HTTP 5xx / 4xx) =================================
class FileStorageError(DbError):
    """Base exception for all file storage errors."""
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4300
    internal_message = (
        "Base unexpected FileStorage exception. "
        "If visible in logs, something went uncaught."
    )


class FileNotFound(FileStorageError):
    http_code = fastapi.status.HTTP_404_NOT_FOUND
    internal_code = 4301
    internal_message = "File does not exist in the data storage folder."


class FileAlreadyExists(FileStorageError):
    http_code = fastapi.status.HTTP_409_CONFLICT
    internal_code = 4302
    internal_message = "Attempted to create a file that already exists."


class FileReadError(FileStorageError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4303
    internal_message = "Error occurred while reading the file from storage."


class FileWriteError(FileStorageError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4304
    internal_message = "Error occurred while writing content to the file."


class FileUpdateError(FileStorageError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4305
    internal_message = "Error occurred while updating or appending content to the file."


class FileDeleteError(FileStorageError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4306
    internal_message = "Error occurred while deleting the file from storage."


class FileListError(FileStorageError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 4307
    internal_message = "Error occurred while listing files in the data storage folder."
