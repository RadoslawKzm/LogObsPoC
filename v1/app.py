import uvicorn
from fastapi import FastAPI

from backend.api.v1.routers import about_router
from backend.api.v1.routers import healthcheck_router



_app = FastAPI(root_path="/api")
_app.include_router(about_router)
_app.include_router(healthcheck_router)


v1_app = _app


"""Didnt do a @app.on_event("startup") decorator.
Sub apps don't invoke startup event handlers, just main app.
https://github.com/tiangolo/fastapi/pull/1554
Lifespan does not work either."""


if __name__ == "__main__":
    """
    Necessary for pycharm debugging purposes.
    If we run your module imported by another (including gunicorn) using something like:
    from manage import app then the value is 'app' or 'manage.app'
    """
    uvicorn.run("app:v1_app", host="0.0.0.0", port=8765)
