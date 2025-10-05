import fastapi

from ._0_500_base import BaseCustomError


# === 1xxx Authentication / Authorization (HTTP4xx) ===
# Base class for all authentication/authorization errors
class AuthError(BaseCustomError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 1000
    external_message = "Authentication or authorization required."
    internal_message = "General authentication/authorization error."


# === 11xx Authentication Errors ===
class AuthenticationError(AuthError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 1100
    external_message = "Authentication failed."
    internal_message = "General authentication failure."


class UnauthorizedError(AuthenticationError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 1101
    external_message = "Invalid or missing authentication."
    internal_message = "Missing or invalid authentication token."


class SessionExpiredError(AuthenticationError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 1102
    external_message = "Session expired. Please log in again."
    internal_message = "User session or token has expired."


class JwtDecodeError(AuthenticationError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 1103
    external_message = "Invalid JWT token."
    internal_message = "Provided JWT token is invalid."


# === 12xx Authorization Errors ===
class AuthorizationError(AuthError):
    http_code = fastapi.status.HTTP_403_FORBIDDEN
    internal_code = 1200
    external_message = "Access forbidden."
    internal_message = "General authorization failure."


class ForbiddenError(AuthorizationError):
    http_code = fastapi.status.HTTP_403_FORBIDDEN
    internal_code = 1201
    external_message = "You do not have permission to access this resource."
    internal_message = "User lacks sufficient permissions."
