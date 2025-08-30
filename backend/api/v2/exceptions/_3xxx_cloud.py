import fastapi

from ._0_500_base import BaseCustomError


# === 3xxx Cloud Errors (HTTP5xx, potentially 4xx on some auth/resource cases)
class CloudError(BaseCustomError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Internal Server Error. Our team is notified."
    internal_code = 3000
    internal_message = "Unhandled Cloud error."


# === 31xx Azure Errors ===
class AzureError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Unexpected error while communicating with Azure cloud."
    internal_code = 31000
    internal_message = "Unhandled Azure error."


class AzureAuthenticationError(AzureError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "Failed to authenticate with Azure cloud."
    internal_code = 31001
    internal_message = "Azure credentials invalid or expired."


class AzureResourceUnavailableError(AzureError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "Azure resource is temporarily unavailable."
    internal_code = 31002
    internal_message = "Azure resource could not be reached or is down."


# === 32xx AWS Errors ===
class AWSError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Unexpected error while communicating with AWS cloud."
    internal_code = 32000
    internal_message = "Unhandled AWS error."


class AWSPermissionDeniedError(AWSError):
    http_code = fastapi.status.HTTP_403_FORBIDDEN
    external_message = "Permission denied for AWS operation."
    internal_code = 32001
    internal_message = "Insufficient AWS IAM permissions."


class AWSServiceTimeoutError(AWSError):
    http_code = fastapi.status.HTTP_504_GATEWAY_TIMEOUT
    external_message = "Timeout while communicating with AWS service."
    internal_code = 32002
    internal_message = "AWS service did not respond within the timeout window."


class AWSRateLimitExceededError(AWSError):
    http_code = fastapi.status.HTTP_429_TOO_MANY_REQUESTS
    external_message = "AWS rate limit exceeded."
    internal_code = 32003
    internal_message = "Too many requests to AWS service in a short time."


# === 33xx GCP Errors ===
class GCPError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    external_message = "Unexpected error while communicating with GCP cloud."
    internal_code = 33000
    internal_message = "Unhandled GCP error."


class GCPAuthenticationError(GCPError):
    http_code = fastapi.status.HTTP_401_UNAUTHORIZED
    external_message = "Failed to authenticate with Google Cloud."
    internal_code = 33001
    internal_message = "GCP credentials invalid or expired."


class GCPQuotaExceededError(GCPError):
    http_code = fastapi.status.HTTP_429_TOO_MANY_REQUESTS
    external_message = "Quota exceeded on Google Cloud service."
    internal_code = 33002
    internal_message = "GCP quota exceeded for this operation."


class GCPServiceUnavailableError(GCPError):
    http_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
    external_message = "Google Cloud service is temporarily unavailable."
    internal_code = 33003
    internal_message = "Service down or unreachable on GCP."
