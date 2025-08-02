import typing

from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.interface import DatabaseInterface
from backend.database.postgres import PostgresSessionManager


class PostgresImplementation(DatabaseInterface):
    database_name = "Postgres"
    session_factory = PostgresSessionManager()

    def __init__(self, *args, session: AsyncSession, **kwargs) -> None:
        self.session: AsyncSession = session

    async def get_record(self) -> str:
        msg: str = "Getting record from Postgres"
        logger.debug(msg)
        return msg

    async def get_many_records(self, *args, **kwargs) -> str:
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

    async def add_record(self, record: typing.Any) -> str:
        msg: str = "Adding record to Postgres"
        logger.debug(msg)
        return msg

    async def add_many_records(self, records: list[typing.Any]) -> str:
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

    async def update_record(self, record: typing.Any):
        msg: str = "Updating record in Postgres"
        logger.debug(msg)
        return msg

    async def update_many_records(self, records: list[typing.Any]) -> str:
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

    async def delete_record(self, record: typing.Any) -> str:
        msg = f"Deleting record in Postgres"
        logger.debug(msg)
        return msg

    async def delete_many_records(self, records: list[typing.Any]) -> str:
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
        msg = f"Deleting many records in Postgres"
        logger.debug(msg)
        return msg
