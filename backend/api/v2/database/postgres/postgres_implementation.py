import typing

from loguru import logger
from backend.api.v2.database.interface import DatabaseInterface
from backend.api.v2.database.postgres.session_manager import PostgresSessionManager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresImplementation(DatabaseInterface):
    database_name = "Postgres"
    session_factory = PostgresSessionManager()

    def __init__(self, *args, session: AsyncSession, **kwargs):
        self.session: AsyncSession = session

    async def get_record(self):
        # self.session.get()
        logger.debug("Getting record from Postgres")

    async def get_many_records(self, *args, **kwargs):
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Getting many records to Postgres")
        result = await self.session.execute(
            text("SELECT id, username, email FROM users")
        )
        rows = result.all()
        # rows is list of sqlalchemy.engine.Row objects, convert to dicts:
        return rows

    async def add_record(self, record: typing.Any):
        logger.debug("Adding record to Postgres")

    async def add_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Adding many records to Postgres")

    async def update_record(self, record: typing.Any):
        logger.debug("Updating record in Postgres")

    async def update_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Updating many records in Postgres")

    async def delete_record(self, record: typing.Any):
        logger.debug("Deleting record in Postgres")

    async def delete_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Deleting many records in Postgres")
