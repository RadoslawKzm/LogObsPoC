from loguru import logger


class FileStorageSessionManager:
    def __init__(self):
        logger.debug("File Storage session manager initialized")

    async def __aenter__(self):
        logger.debug("File Storage  session manager __aenter__")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug("File Storage  session manager __aexit__")
