import fastapi

from .._0_500_base import BaseCustomError


# === 5xxx Cloud Errors (HTTP5xx, potentially 4xx on some auth/resource cases)
class CloudError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 5000
    external_message = "Internal server error. Our team has been notified."
    internal_message = "Unhandled Cloud error."