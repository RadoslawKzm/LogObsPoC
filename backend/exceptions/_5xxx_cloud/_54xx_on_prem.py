import fastapi

from ._5000_base import CloudError


# === 54xx On Premises Infra Errors ===
class OnPremError(CloudError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 5400
    internal_message = (
        "Unexpected error while communicating with internal infrastructure."
    )

class TestError(OnPremError):
    http_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = 5401
    internal_message = (
        "Unexpected error while communicating with internal infrastructure."
    )
