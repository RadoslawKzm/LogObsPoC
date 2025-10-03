import typing

import fastapi

from ._0_500_base import BaseCustomError


# === 2xxx API Errors ===
class ApiError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 2000
    external_message = "Internal server error. Our team has been notified."
    internal_message = "General API error."

    _api_errors: typing.ClassVar[dict] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._api_errors[cls.__name__] = cls.openapi()


# === 21xx Input / Validation (HTTP 4xx) ===
class InvalidInputError(ApiError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 2100
    external_message = "Invalid input provided."
    internal_message = "Malformed or invalid request data."


class MissingFieldError(InvalidInputError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 2101
    external_message = "Missing required field."
    internal_message = "Mandatory field missing in request payload."


class FieldFormatError(InvalidInputError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    internal_code = 2102
    external_message = "Incorrect field format."
    internal_message = "One or more fields violate validation rules."


class NotFoundError(InvalidInputError):
    http_code = fastapi.status.HTTP_404_NOT_FOUND
    internal_code = 2103
    external_message = "Requested resource not found."
    internal_message = "Resource does not exist or is inaccessible."


class RequestConflictError(InvalidInputError):
    http_code = fastapi.status.HTTP_409_CONFLICT
    internal_code = 2104
    external_message = "Request conflict."
    internal_message = "Request conflicts with the current resource state."


# === 22xx API Internal Server Errors (HTTP 5xx) ===
class UnknownServerError(ApiError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 2200
    external_message = "Unexpected server error."
    internal_message = "Unhandled exception in API server."


class ExternalServiceUnavailableError(UnknownServerError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 2201
    external_message = "External service unavailable."
    internal_message = "Dependent external service is down or unreachable."


class RequestTimeoutError(UnknownServerError):
    http_code = fastapi.status.HTTP_504_GATEWAY_TIMEOUT
    internal_code = 2202
    external_message = "Request timed out."
    internal_message = (
        "API request exceeded timeout while waiting for a response."
    )


class ConfigurationError(UnknownServerError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 2203
    external_message = "Configuration error."
    internal_message = (
        "API configuration or environment is invalid or missing."
    )
