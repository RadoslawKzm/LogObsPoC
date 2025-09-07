import typing
import pydantic

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, create_engine, select, text

from backend.database.interface import DatabaseInterface
from backend.database.postgres import PostgresSessionManager
from backend.database.config import pg_config
from backend.database.postgres.models import tables

COLUMN_NAME = str
COLUMN_VALUE = str

T = typing.TypeVar("T", bound=SQLModel)


class PostgresImplementation(DatabaseInterface):
    database_name = "Postgres"
    session_factory = PostgresSessionManager

    def __init__(self, *args, session: AsyncSession, **kwargs) -> None:
        self.session: AsyncSession = session

    async def get_record(
        self,
        key: str = None,
        value: str = None,
        place: str = None,
    ) -> T | False:
        logger.opt(lazy=True).debug(
            "Getting key:{key} value:{value} ," "place:{place}",
            key=lambda: key,
            value=lambda: value,
            place=lambda: place,
        )
        table = tables.get(place, None)
        if table is None:
            return None
        statement = select(table).where(getattr(table, key) == value)
        results = await self.session.execute(statement)
        result = results.scalars().first()
        return result or None

    async def get_many_records(self, *args, **kwargs) -> list[T | None]:
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """
        msg: str = "Getting many records from Postgres"
        logger.debug(msg)
        return msg

        # logger.debug("Getting many records to Postgres")
        # result = await self.session.execute(
        #     text("SELECT id, username, email FROM users")
        # )
        # rows = result.all()
        # # rows is list of sqlalchemy.engine.Row objects, convert to dicts:
        # return rows

    async def list_records(
        self,
        start: int,
        size: int,
    ) -> typing.List[typing.Any]:
        """Implement function that returns all available records.
        Implement simple pagination with start pointer and size.
        """
        pass

    async def add_record(
        self,
        *args,
        body: pydantic.BaseModel,
        place: str,
        **kwargs,
    ) -> T | False:
        table = tables.get(place, None)
        if table is None:
            return None
        try:
            record = self.session.add(body)
        except Exception:
            return None
        return record

    async def add_many_records(self, *args, **kwargs) -> str:
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """
        msg: str = "Adding many records to Postgres"
        logger.debug(msg)
        return msg

    async def update_record(self, *args, **kwargs):
        msg: str = "Updating record in Postgres"
        logger.debug(msg)
        return msg

    async def update_many_records(self, *args, **kwargs) -> str:
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """
        msg: str = "Updating many records in Postgres"
        logger.debug(msg)
        return msg

    async def delete_record(self, *args, **kwargs) -> str:
        msg = "Deleting record in Postgres"
        logger.debug(msg)
        return msg

    async def delete_many_records(self, *args, **kwargs) -> str:
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
        msg = "Deleting many records in Postgres"
        logger.debug(msg)
        return msg

    @classmethod
    def init_db(cls):
        """
        Initialize Postgres database:
        - Create all tables defined with SQLModel if they don't exist.
        """
        engine = create_engine(pg_config.sync_url, echo=False)
        SQLModel.metadata.create_all(engine, checkfirst=True)
        logger.debug("Postgres tables initialized successfully.")
