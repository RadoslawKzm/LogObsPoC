from sqlalchemy.ext.asyncio import AsyncSession
import time
from loguru import logger

class InstrumentedAsyncSession(AsyncSession):
    async def execute(self, *args, **kwargs):
        start = time.perf_counter()
        try:
            return await super().execute(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            logger.debug(f"{args[0].text}: Time={duration:.4f}s")

    async def commit(self):
        start = time.perf_counter()
        try:
            return await super().commit()
        finally:
            duration = time.perf_counter() - start
            logger.debug(f"Session.commit took {duration:.4f}s")

    async def flush(self, *args, **kwargs):
        start = time.perf_counter()
        try:
            return await super().flush(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            logger.debug(f"Session.flush took {duration:.4f}s")