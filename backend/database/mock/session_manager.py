from loguru import logger


class MockSessionManager:
    def __init__(self):
        logger.debug("Mock session manager initialized")

    async def __aenter__(self):
        logger.debug("Mock session manager __aenter__")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Mock session manager __aexit__")
