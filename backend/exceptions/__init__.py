import pathlib

from . import _1xxx_auth as auth
from . import _2xxx_api as api
from . import _3xxx_core as core
from . import _4xxx_db as db
from . import _5xxx_cloud as cloud
from ._0_500_base import BaseCustomError
from .exception_handlers import add_handlers
from .generate_docs import build_readme

markdown = build_readme()
current_folder = pathlib.Path(__file__).parent
with open(current_folder / "README_internal_codes.md", "w") as f:
    f.write(markdown)
