import fastapi

from ._0_500_base import BaseCustomError

# === 4xxx Core Errors (HTTP5xx) ===


class CoreError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Internal Server Error. Our team is notified."
    internal_code = 4000
    internal_message = "Internal Server Error. Our team is notified."


class UnexpectedError(CoreError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Something went wrong."
    internal_code = 4100
    internal_message = "Unexpected failure in core logic."


class ConfigurationError(CoreError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Server misconfiguration."
    internal_code = 4200
    internal_message = "Critical configuration value missing or invalid."


class ResourceConflictError(CoreError):
    http_code = fastapi.status.HTTP_409_CONFLICT
    external_message = "Conflict with current state."
    internal_code = 4300
    internal_message = "Resource state conflict check concurrency, versioning."


class ExternalServiceError(CoreError):
    http_code = fastapi.status.HTTP_502_BAD_GATEWAY
    external_message = "Upstream service unavailable."
    internal_code = 4400
    internal_message = "Failed communication with external dependency."


class TimeoutError(CoreError):
    http_code = fastapi.status.HTTP_504_GATEWAY_TIMEOUT
    external_message = "Server timeout."
    internal_code = 4500
    internal_message = "The request took too long to complete."


class DataInconsistencyError(CoreError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Data inconsistency detected."
    internal_code = 4600
    internal_message = "Application-level integrity constraint violated."


class FeatureDisabledError(CoreError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "This feature is temporarily disabled."
    internal_code = 4700
    internal_message = (
        "Feature has been intentionally disabled by system configuration."
    )
