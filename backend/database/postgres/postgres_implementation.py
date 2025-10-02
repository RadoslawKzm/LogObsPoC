import typing


from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, create_engine, select, delete

from backend.database.interface import DatabaseInterface
from backend.database.postgres import PostgresSessionManager
from backend.database.config import pg_config
from backend.database.postgres.models import tables
from backend.exceptions import db_exceptions

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
        key: str,
        value: str,
        place: str,
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

    async def get_many_records(
        self,
        page_num: int,
        page_size: int,
        place: str,
    ) -> list[T] | None:
        """Need to be separate from get_record.
        *This function returns requested page_size + 1*
        Reasoning: It indicates if there is more items for next page.
        Edge case: you get all records remaining but result size==page_size.
        This way you send user page link that will have no results.
        Using this function please: trim last record in list.
        1. Check if returned size is page_size+1.
        - If yes means next page is available.
        - If not means this is your last page.
        2. Trim last record in list if above page_size
        """
        logger.opt(lazy=True).debug(
            "Getting place:{place}",
            place=lambda: place,
        )
        table = tables.get(place, None)
        if table is None:
            return None
        offset: int = (page_num - 1) * page_size
        statement = select(table).offset(offset).limit(page_size + 1)
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return results or None

    async def add_record(
        self,
        data: T,
        place: str,
    ) -> T | None:
        table: type[SQLModel] = tables.get(place, None)
        if table is None:
            return None
        db_record = table.model_validate(data)
        try:
            self.session.add(db_record)
            await self.session.commit()
            await self.session.refresh(db_record)
        except Exception as exc:
            exc = db_exceptions.sql.AddRecordError
            msg: str = f"Record: {data.model_dump()}"
            raise exc(internal_message=f"{exc} {msg}") from exc
        return db_record

    async def add_many_records(
        self,
        records: list[T],
        place: str,
    ) -> str:
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

    async def update_record(self, data: T, place: str) -> T:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def update_many_records(self, data: list[T], place: str) -> str:
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

    async def delete_record(
        self,
        key: str,
        value: str,
        place: str,
    ) -> int | bool:
        table: type[SQLModel] = tables.get(place, None)
        if table is None:
            return False
        statement = delete(table).where(getattr(table, key) == value)
        try:
            result = await self.session.execute(statement)
            await self.session.commit()
        except Exception as exc:
            raise db_exceptions.DbError from exc
        return result.rowcount  # result.rowcount number of rows affected

    async def delete_many_records(
        self,
        data: list[T],
        place: str,
    ) -> str:
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
