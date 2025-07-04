import typing

from loguru import logger
from backend.database.interface import DatabaseInterface
from backend.database.mongo.session_manager import MongoSessionManager


class MongoImplementation(DatabaseInterface):
    database_name = "Mongo"
    session_factory = MongoSessionManager()

    def __init__(self, *args, session, **kwargs):
        self.session = session

    async def get_record(self):
        logger.debug("Getting record from Mongo")

    async def get_many_records(self):
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Getting many records to Mongo")

    async def add_record(self, record: typing.Any):
        logger.debug("Adding record to Mongo")

    async def add_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Adding many records to Mongo")

    async def update_record(self, record: typing.Any):
        logger.debug("Updating record in Mongo")

    async def update_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Updating many records in Mongo")

    async def delete_record(self, record: typing.Any):
        logger.debug("Deleting record in Mongo")

    async def delete_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Deleting many records in Mongo")
