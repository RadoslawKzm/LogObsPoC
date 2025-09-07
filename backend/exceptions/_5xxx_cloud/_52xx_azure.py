import fastapi

from ._5000_base import CloudError

# === 52xx Azure Errors ===
class AzureError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 5200
    external_message = "Unexpected error while communicating with Azure cloud."
    internal_message = "Unhandled Azure error."


class AzureAuthenticationError(AzureError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    internal_code = 5201
    external_message = "Failed to authenticate with Azure cloud."
    internal_message = "Azure credentials invalid or expired."


class AzureResourceUnavailableError(AzureError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    internal_code = 5202
    external_message = "Azure resource is temporarily unavailable."
    internal_message = "Azure resource could not be reached or is down."

