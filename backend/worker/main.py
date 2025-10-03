import asyncio

import uvicorn

from backend.worker import app
from backend.worker.config import worker_settings

if __name__ == "__main__":
    """
    Necessary for pycharm debugging purposes.
    If we run your module imported by another
        (including gunicorn) using something like:
    from manage import app then the value is 'app' or 'manage.app'
    """
    config = uvicorn.Config(
        app=app,
        host=worker_settings.WORKER_API_HOST,
        port=worker_settings.WORKER_API_PORT,
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())  # no loop_factory here


# sudo lsof -i tcp:8765
# kill -15 (its soft) PID
# kill -9 (hardcore) PID
# lsof -i -P | grep :$PORT

# uvicorn.run(
#     app=app,
#     host=worker_settings.WORKER_API_HOST,
#     port=worker_settings.WORKER_API_PORT,
#     log_config=None,
#     access_log=False,
#     # log_level="critical"
#     # reload=True,
# )
