import uvicorn
from loguru import logger
import env

if __name__ == "__main__":
    """
    Necessary for pycharm debugging purposes.
    If we run your module imported by another
        (including gunicorn) using something like:
    from manage import app then the value is 'app' or 'manage.app'
    """
    host: str = "0.0.0.0"
    port: int = 8765
    logger.info("App is loading!")
    logger.info("Started server process")
    logger.info("Waiting for application startup.")
    uvicorn.run(
        "app:app",
        host=env.APP_HOST,
        port=env.APP_PORT,
        log_config=None,
        access_log=False,
        # log_level="critical"
        # reload=True,
    )


# sudo lsof -i tcp:8765
# kill -15 (its soft) PID
# kill -9 (hardcore) PID
# lsof -i -P | grep :$PORT
