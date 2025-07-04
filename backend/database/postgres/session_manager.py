import sqlalchemy.exc
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel
from loguru import logger

from backend.database.config import databases, Database
from backend.proj_exc import db_exceptions
from backend.database.postgres.session_measurement import InstrumentedAsyncSession

Base = declarative_base()


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
        database=None,
        suppress_exc: bool = False,
        **kwargs,
    ) -> None:
        logger.debug("Initializing Postgres session manager")
        self.database = database
        db_opt = databases["postgres"]
        db_url: str = (
            f"{db_opt.async_driver}://"
            f"{db_opt.user}:{db_opt.password}@"
            f"{db_opt.hostname}:{db_opt.port}/{db_opt.db_name}"
        )
        self.engine: AsyncEngine = create_async_engine(
            url=db_url,
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

    # async def create_and_populate_mock_db(self):
    #     create_table_sql = """
    #     CREATE TABLE IF NOT EXISTS users (
    #         id SERIAL PRIMARY KEY,
    #         username VARCHAR(50) UNIQUE NOT NULL,
    #         email VARCHAR(255) UNIQUE NOT NULL
    #     );
    #     """
    #
    #     insert_sql = """
    #     INSERT INTO users (username, email) VALUES
    #         ('alice', 'alice@example.com'),
    #         ('bob', 'bob@example.com')
    #     ON CONFLICT (username) DO NOTHING;
    #     """
    #
    #     async with self.session as session:
    #         await session.execute(text(create_table_sql))
    #         await session.execute(text(insert_sql))
    #         await session.commit()

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
            raise RuntimeError("PostgresSessionManager is not initialized")
        async with cls._instance as session:
            yield session
