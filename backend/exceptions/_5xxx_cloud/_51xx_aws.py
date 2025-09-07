import fastapi
from ._5000_base import CloudError

# === 51xx AWS Errors ===
class AWSError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 5100
    external_message = "Unexpected error while communicating with AWS cloud."
    internal_message = "Unhandled AWS error."


class AWSPermissionDeniedError(AWSError):
    http_code = fastapi.status.HTTP_403_FORBIDDEN
    internal_code = 5101
    external_message = "Permission denied for AWS operation."
    internal_message = "Insufficient AWS IAM permissions."


class AWSServiceTimeoutError(AWSError):
    http_code = fastapi.status.HTTP_504_GATEWAY_TIMEOUT
    internal_code = 5102
    external_message = "Timeout while communicating with AWS service."
    internal_message = "AWS service did not respond within the timeout window."


class AWSRateLimitExceededError(AWSError):
    http_code = fastapi.status.HTTP_429_TOO_MANY_REQUESTS
    internal_code = 5103
    external_message = "AWS rate limit exceeded."
    internal_message = "Too many requests to AWS service in a short time."