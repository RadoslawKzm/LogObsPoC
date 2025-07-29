import fastapi

from .base import BaseCustomError

# === 5xxx Authentication / Authorization (HTTP4xx) ===

# Base class for all authentication/authorization errors
class AuthError(BaseCustomError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "You are not authorized."
    internal_code = 5000
    internal_message = "Unauthorized request."


# === 51xx Authentication Errors ===

class AuthenticationError(AuthError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "You are not authorized."
    internal_code = 5100
    internal_message = "General authentication failure."


class UnauthorizedError(AuthenticationError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "You are not authorized."
    internal_code = 5101
    internal_message = "Unauthorized request."


class SessionExpiredError(AuthenticationError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "Session expired. Please log in again."
    internal_code = 5102
    internal_message = "User session or token has expired."


# === 52xx Authorization Errors ===

class AuthorizationError(AuthError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "You are not authorized."
    internal_code = 5200
    internal_message = "General authorization failure."


class ForbiddenError(AuthorizationError):
    http_code = fastapi.status.HTTP_403_FORBIDDEN
    external_message = "Access forbidden."
    internal_code = 5201
    internal_message = "User lacks sufficient permissions."
