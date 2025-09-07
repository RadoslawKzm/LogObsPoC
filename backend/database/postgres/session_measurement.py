import time

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Executable


class InstrumentedAsyncSession(AsyncSession):
    async def execute(self, statement: Executable, *args, **kwargs):
        start = time.perf_counter()
        try:
            return await super().execute(statement, *args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            sql_str: str = str(statement).replace("\n", "")
            logger.debug(f"SQL: {sql_str} | Duration: {duration:.4f}s")

    async def commit(self):
        start = time.perf_counter()
        try:
            return await super().commit()
        finally:
            duration = time.perf_counter() - start
            logger.debug(f"Session.commit | Duration: {duration:.4f}s")

    async def flush(self, *args, **kwargs):
        start = time.perf_counter()
        try:
            return await super().flush(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            logger.debug(f"Session.flush | Duration: {duration:.4f}s")
