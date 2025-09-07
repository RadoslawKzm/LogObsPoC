import typing

from loguru import logger

from backend.database.interface import DatabaseInterface
from backend.database.mongo import MongoSessionManager


class MongoImplementation(DatabaseInterface):
    database_name = "Mongo"
    session_factory = MongoSessionManager

    def __init__(self, *args, session, **kwargs) -> None:
        self.session = session

    async def get_record(self) -> str:
        msg: str = "Getting record from Mongo"
        logger.debug(msg)
        return msg

    async def get_many_records(self) -> str:
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """
        msg: str = "Getting many records from Mongo"
        logger.debug(msg)
        return msg

    async def add_record(self, record: typing.Any) -> str:
        msg: str = "Adding record to Mongo"
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
        msg: str = "Adding many records to Mongo"
        logger.debug(msg)
        return msg

    async def update_record(self, record: typing.Any) -> str:
        msg: str = "Updating record in Mongo"
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
        msg: str = "Updating many records in Mongo"
        logger.debug(msg)
        return msg

    async def delete_record(self, record: typing.Any):
        msg: str = "Deleting record from Mongo"
        logger.debug(msg)
        return msg

    async def delete_many_records(self, records: list[typing.Any]):
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
        msg: str = "Deleting many records in Mongo"
        logger.debug(msg)
        return msg
