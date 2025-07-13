import fastapi

from backend.api.v2.exc.base import BaseCustomError


class ApiError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Internal Server Error. Our team is notified."
    internal_code = 1000
    internal_message = "Unexpected API error. This should not happen."


# === 11xx Authentication / Authorization (HTTP4xx) ===
class UnauthorizedError(ApiError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "You are not authorized."
    internal_code = 1100
    internal_message = "Unauthorized request."


class ForbiddenError(ApiError):
    http_code = fastapi.status.HTTP_403_FORBIDDEN
    external_message = "Access forbidden."
    internal_code = 1101
    internal_message = "User lacks sufficient permissions."


class SessionExpiredError(ApiError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "Session expired. Please log in again."
    internal_code = 1102
    internal_message = "User session or token has expired."


# === 12xx Input / Validation (HTTP4xx) ===
class InvalidInputError(ApiError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Invalid input provided."
    internal_code = 1200
    internal_message = "Malformed or invalid request data."


class MissingFieldError(ApiError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Missing required field."
    internal_code = 1201
    internal_message = "Mandatory field missing in request payload."


class FieldFormatError(ApiError):
    http_code = fastapi.status.HTTP_400_BAD_REQUEST
    external_message = "Incorrect field format."
    internal_code = 1202
    internal_message = "One or more fields violate validation rules."


class ResourceNotFoundError(ApiError):
    http_code = fastapi.status.HTTP_404_NOT_FOUND
    external_message = "Requested resource not found."
    internal_code = 1203
    internal_message = "Resource does not exist or is inaccessible."


class RequestConflictError(ApiError):
    http_code = fastapi.status.HTTP_409_CONFLICT
    external_message = "Request conflict."
    internal_code = 1204
    internal_message = "Request conflicts with resource state."


class UnknownServerError(ApiError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Server encountered an unexpected error."
    internal_code = 1300
    internal_message = "Unexpected error in API server."


# === 13xx API Internal Server Errors (HTTP 5xx) ===
class ExternalServiceUnavailableError(ApiError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "External service unavailable."
    internal_code = 1301
    internal_message = "Dependent external service is down or unreachable."


class RequestTimeoutError(ApiError):
    http_code = fastapi.status.HTTP_504_GATEWAY_TIMEOUT
    external_message = "Request timed out."
    internal_code = 1302
    internal_message = "API request timed out waiting for a response."


class ConfigurationError(ApiError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Configuration error detected."
    internal_code = 1303
    internal_message = (
        "API configuration or environment is invalid or missing."
    )
