from typing import Any, Dict, Optional, Union

from fastapi import status

response_200: Optional[Dict[Union[int, str], Dict[str, Any]]] = {
    "200": {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "normal": {
                        "summary": "Health check OK",
                        "value": {
                            "status_code": status.HTTP_200_OK,
                            "content": {"data": "version_v1"},
                        },
                    },
                }
            }
        },
    },
}
