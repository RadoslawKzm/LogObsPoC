import fastapi

from ._5000_base import CloudError

# === 53xx GCP Errors ===
class GCPError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 5300
    external_message = "Unexpected error while communicating with GCP cloud."
    internal_message = "Unhandled GCP error."


class GCPAuthenticationError(GCPError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 5301
    external_message = "Failed to authenticate with Google Cloud."
    internal_message = "GCP credentials invalid or expired."


class GCPQuotaExceededError(GCPError):
    http_code = fastapi.status.HTTP_429_TOO_MANY_REQUESTS
    internal_code = 5302
    external_message = "Quota exceeded on Google Cloud service."
    internal_message = "GCP quota exceeded for this operation."


class GCPServiceUnavailableError(GCPError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 5303
    external_message = "Google Cloud service is temporarily unavailable."
    internal_message = "Service down or unreachable on GCP."
