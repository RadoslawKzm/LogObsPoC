from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from backend.exceptions import db_exceptions
from backend.database.config import pg_config
from backend.database.postgres.session_measurement import (
    InstrumentedAsyncSession,
)
from sqlmodel.ext.asyncio.session import AsyncSession


class PostgresSessionManager:
    """
    Context manager class for managing SQLAlchemy session objects.
    It manages opening transactions, returns session object,
    then after transaction commits/rollbacks and closes.
    It manages all fallbacks for user.
    UserCore doesn't need to worry
        about committing changes to DB and exception handling.
    """

    _instance = None

    def __init__(
        self,
        *args,
        suppress_exc: bool = False,
        **kwargs,
    ) -> None:
        logger.debug("Initializing Postgres session manager")
        self.engine: AsyncEngine = create_async_engine(
            url=pg_config.async_url,
            pool_size=50,
            max_overflow=20,
        )
        self.suppress_exc = suppress_exc
        self.async_session_factory = async_sessionmaker(
            *args,
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            class_=InstrumentedAsyncSession,
            **kwargs,
        )

    async def __aenter__(self) -> AsyncSession:
        """
        :return: SQLAlchemy session object for context manager to operate on.
        """
        logger.debug("Postgres session manager __aenter__")
        self.session: AsyncSession = self.async_session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Postgres session manager __aexit__")
        if any((exc_type, exc_val, exc_tb)):
            if isinstance(exc_val, db_exceptions.sql.FlowControlError):
                # Forwarding dev control flow exceptions giving HTTP4xx
                raise exc_val
            logger.opt(exception=exc_val).error("Error in DB session occurred")
            logger.debug("Rolling back session")
            await self.session.rollback()
            logger.debug("Session rolled back successfully.")
            logger.debug("Closing DB session")
            await self.session.close()
            logger.debug("Session closed successfully.")
            if self.suppress_exc:
                logger.opt(lazy=True).debug(
                    "Suppressing exception because suppress={x}",
                    x=lambda: self.suppress_exc,
                )
                return self.suppress_exc  # gracefully suppressing if True
            raise db_exceptions.sql.SQLError from exc_val

        try:
            await self.session.commit()
        except Exception as exc_info:
            await self.session.rollback()
            raise db_exceptions.DbError(
                internal_message="Unexpected exception in __exit__"
                " while trying to commit session."
            ) from exc_info
        finally:
            await self.session.close()

    async def close(self):
        await self.engine.dispose()
