import pathlib
from .generate_docs import build_readme

from ._0_500_base import BaseCustomError
from . import _1xxx_auth as auth_exceptions
from . import _2xxx_api as api_exceptions
from . import _3xxx_core as core_exceptions
from . import _4xxx_db as db_exceptions
from . import _5xxx_cloud as cloud_exceptions
from .exception_handlers import add_exception_handlers

__all__ = [
    api_exceptions,
    db_exceptions,
    auth_exceptions,
    core_exceptions,
    cloud_exceptions,
]


markdown = build_readme()
current_folder = pathlib.Path(__file__).parent
with open(current_folder / "README_internal_codes.md", "w") as f:
    f.write(markdown)
