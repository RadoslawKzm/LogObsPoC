from loguru import logger


class MongoSessionManager:
    def __init__(self):
        logger.debug("Mongo session manager initialized")

    async def __aenter__(self):
        logger.debug("Mongo session manager __aenter__")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Mongo session manager __aexit__")
