from . import api as api_exceptions
from . import base as base_exceptions
from . import db as db_exceptions
from . import auth as auth_exceptions
from . import core as core_exceptions
from . import cloud as cloud_exceptions
from .base import BaseCustomError
from .exception_handlers import add_exception_handlers

__all__ = [
api_exceptions,
    db_exceptions,
    auth_exceptions,
    core_exceptions,
    cloud_exceptions,
]
# MODULE_NAME = str
# INTERNAL_CODE = int
#
# EXCEPTION_REGISTRY: dict[MODULE_NAME, dict[INTERNAL_CODE, dict]] = {}
#
# for module in [
#     api_exceptions,
#     db_exceptions,
#     auth_exceptions,
#     core_exceptions,
#     cloud_exceptions,
# ]:
#     for name in dir(module):
#         obj = getattr(module, name)
#         if (
#             isinstance(obj, type)
#             and issubclass(obj, base_exceptions.BaseCustomError)
#             and obj is not base_exceptions.BaseCustomError
#         ):
#             internal_code = obj.internal_code
#             if internal_code in EXCEPTION_REGISTRY:
#                 raise ValueError(
#                     f"Duplicate internal code: {internal_code} in {obj.__name__}"
#                 )
#             EXCEPTION_REGISTRY[name][internal_code] = {
#                 "exception_class": obj,
#                 "module": module.__name__,
#                 "name": obj.__name__,
#             }


from pydantic import BaseModel, Field
from typing import Optional, Dict, Type


class ErrorDoc(BaseModel):
    internal_code: int = Field(..., description="Internal code used for tracking")
    http_code: int = Field(..., description="HTTP response code")
    internal_message: str = Field(..., description="Detailed internal log message")
    external_message: str = Field(..., description="User-facing error message")
    exception_class: str = Field(..., description="Name of the exception class")
    module: str = Field(..., description="Module in which the error is defined")
    members: Optional[Dict[str, 'ErrorDoc']] = Field(
        None, description="Nested error documentation"
    )

    class Config:
        arbitrary_types_allowed = True


# Allow self-referencing models
ErrorDoc.model_rebuild()

# from collections import defaultdict
# # Final result
# DOCUMENTED_EXCEPTIONS = defaultdict(dict)
#
# # Used to check for duplicates
# seen_internal_codes = set()
#
# for module in __all__:
#     for name in dir(module):
#         if name.startswith("__"):
#             continue
#         obj = getattr(module, name)
#         if (
#             isinstance(obj, type)
#             and issubclass(obj, base_exceptions.BaseCustomError)
#             and obj is not base_exceptions.BaseCustomError
#         ):
#             internal_code = obj.internal_code
#             base_name = obj.__bases__[0].__name__
#
#             if internal_code in seen_internal_codes:
#                 raise ValueError(f"Duplicate internal code: {internal_code} in {obj.__name__}")
#             seen_internal_codes.add(internal_code)
#
#             DOCUMENTED_EXCEPTIONS[base_name][internal_code] = {
#                 "exception_class": obj,
#                 "module": module.__name__,
#                 "name": obj.__name__,
#                 "description": obj.__doc__.strip() if obj.__doc__ else "",
#                 "status_code": getattr(obj, "status_code", None),
#             }
#             # doc = ErrorDoc(
#             #     internal_code=obj.internal_code,
#             #     http_code=obj.http_code,
#             #     internal_message=obj.internal_message,
#             #     external_message=obj.external_message,
#             #     exception_class=obj.__name__,
#             #     module=module.__name__,
#             # )
# Tree output
EXCEPTION_TREE = {}

# Duplicate tracking
seen_internal_codes = set()

# Helper function to insert into the tree based on inheritance
def insert_exception(exception_cls, module):
    # Get full MRO up to (but not including) BaseCustomError
    mro = [
        base.__name__
        for base in exception_cls.__mro__
        if issubclass(base, base_exceptions.BaseCustomError) and base is not base_exceptions.BaseCustomError
    ][::-1]  # reverse to get from top to bottom

    # Root of tree
    current = EXCEPTION_TREE

    # Walk down the hierarchy
    for base_name in mro:
        if base_name not in current:
            current[base_name] = {}
        current = current[base_name]

    # Leaf: add this specific exception by its internal code
    internal_code = exception_cls.internal_code
    if internal_code in seen_internal_codes:
        raise ValueError(f"Duplicate internal code: {internal_code} in {exception_cls.__name__}")
    seen_internal_codes.add(internal_code)

    current[internal_code] = {
        "exception_class": exception_cls,
        "module": module.__name__,
        "name": exception_cls.__name__,
        "description": exception_cls.__doc__.strip() if exception_cls.__doc__ else "",
        "status_code": getattr(exception_cls, "status_code", None),
    }

# Now walk through all modules to collect exceptions
for module in __all__:
    for name in dir(module):
        if name.startswith("__"):
            continue
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, base_exceptions.BaseCustomError)
            and obj is not base_exceptions.BaseCustomError
        ):
            insert_exception(obj, module)
