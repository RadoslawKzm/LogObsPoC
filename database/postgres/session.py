import sqlalchemy.exc
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel

from exc import db_exceptions
from database.registry import Database

Base = declarative_base()


class DbManager(AsyncSession):
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
        database: Database,
        suppress_exc: bool = False,
        **kwargs,
    ) -> None:
        self._args = args
        self._kwargs = kwargs
        self.database = database
        self.engine: AsyncEngine = create_async_engine(
            url=database.async_conn_string,
            pool_size=50,
            max_overflow=20,
        )
        self.suppress_exc = suppress_exc
        super(DbManager, self).__init__(
            *args,
            autocommit=False,
            bind=self.engine,
            autoflush=False,
            # expire_on_commit=False,
            **kwargs,
        )

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DbManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def init_db(cls, database: Database) -> None:
        engine = create_engine(
            database.sync_conn_string,
        )
        # from sqlalchemy_utils import drop_database
        # if database_exists(engine.url):
        #     drop_database(engine.url)
        if not database_exists(engine.url):
            create_database(engine.url)
        SQLModel.metadata.create_all(engine)

    async def __aenter__(self) -> AsyncSession:
        """
        :return: SQLAlchemy session object for context manager to operate on.
        """
        self.session = self
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if any((exc_type, exc_val, exc_tb)):
            if isinstance(exc_val, db_exceptions.ManualDbException):
                # Forwarding dev control flow exceptions giving HTTP4xx
                raise exc_val
            if not isinstance(exc_val, sqlalchemy.exc.SQLAlchemyError):
                # Forwarding any non DB exception
                raise exc_val
            logger.opt(exception=exc_val).error(
                "Error in DB session occurred."
            )
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
            # Matching unexpected exceptions giving HTTP5xx
            if isinstance(exc_val, sqlalchemy.exc.OperationalError):
                raise db_exceptions.OperationalException()
            if isinstance(exc_val, sqlalchemy.exc.IntegrityError):
                raise db_exceptions.IntegrityException()
            if isinstance(exc_val, sqlalchemy.exc.DataError):
                raise db_exceptions.DataException()
            if isinstance(exc_val, sqlalchemy.exc.ProgrammingError):
                raise db_exceptions.ProgrammingException()
            if isinstance(exc_val, sqlalchemy.exc.DatabaseError):
                raise db_exceptions.DatabaseException()
            raise db_exceptions.UnexpectedException from exc_val

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise db_exceptions.DbException(
                internal_message="Unexpected exception in __exit__"
                " while trying to commit session."
            )
        finally:
            await self.session.close()

    async def close(self):
        await self.engine.dispose()

    @classmethod
    async def get_session(cls):
        if cls._instance is None:
            raise RuntimeError("DbManager is not initialized")
        async with cls._instance as session:
            yield session
