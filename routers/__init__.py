from .about.endpoints import about_router as about
from .healthcheck.endpoints import healthcheck_router as healthcheck
from .api_exceptions.endpoints import api_exceptions_router
from .db_exceptions.endpoints import db_exceptions_router

__all__: list = [about, healthcheck]
