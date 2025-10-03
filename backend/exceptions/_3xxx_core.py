import fastapi

from ._0_500_base import BaseCustomError


# === 3xxx Core Errors (HTTP 5xx) ===
class CoreError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 3000
    internal_message = "General core error."


class UnexpectedError(CoreError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 3001
    internal_message = "Unhandled failure in core logic."


class ConfigurationError(CoreError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 3002
    internal_message = "Critical configuration value missing or invalid."


class ResourceConflictError(CoreError):
    http_code = fastapi.status.HTTP_409_CONFLICT
    internal_code = 3003
    internal_message = (
        "Conflict with current resource state."
        "Possibly due to concurrency or version mismatch."
    )


class ExternalServiceError(CoreError):
    http_code = fastapi.status.HTTP_502_BAD_GATEWAY
    internal_code = 3004
    internal_message = "Failed communication with an upstream dependency."


class TimeoutError(CoreError):
    http_code = fastapi.status.HTTP_504_GATEWAY_TIMEOUT
    internal_code = 3005
    internal_message = "Request exceeded the allowed time limit."


class DataInconsistencyError(CoreError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 3006
    internal_message = (
        "Application-level integrity or consistency check failed."
    )


class FeatureDisabledError(CoreError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 3007
    internal_message = "Feature has been disabled by system configuration."
