import typing

from loguru import logger

from backend.exceptions import db_exceptions
from backend.database.interface import DatabaseInterface
from backend.database.mock import MockSessionManager

from .database import books


class MockImplementation(DatabaseInterface):
    database_name = "Mock"
    session_factory = MockSessionManager()

    def __init__(self, *args, session, **kwargs) -> None:
        self.session = session

    async def get_record(self, record_id: int) -> dict:
        logger.debug("Getting record from Mock Database")
        book = books.get(record_id, None)
        if not book:
            msg: str = f"No book with id {record_id} found"
            raise db_exceptions.RecordNotFoundError(
                internal_message=msg,
                external_message=msg,
            )
        return book

    async def get_many_records(self) -> list[dict]:
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Getting many records from Mock Database")
        return list(books.values())

    async def add_record(self, record: typing.Any) -> str:
        logger.debug("Adding record to Mock Database")
        msg: str = "Adding record to Mock Database"
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
        msg: str = "Adding many records to Mock Database"
        logger.debug(msg)
        return msg

    async def update_record(self, record: typing.Any) -> str:
        msg: str = "Updating record in Mock Database"
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
        msg: str = "Updating many records in Mock Database"
        logger.debug(msg)
        return msg

    async def delete_record(self, record_id: int) -> None:
        logger.debug("Deleting record in Mock Database")
        book = books.get(record_id, None)
        if not book:
            msg: str = f"No book with id {record_id} found"
            raise db_exceptions.RecordNotFoundError(
                internal_message=msg,
                external_message=msg,
            )
        del books[record_id]

    async def delete_many_records(self, *args) -> None:
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
        logger.debug("Deleting many records in Mock Database")
        for record_id in list(books.keys()):
            del books[record_id]
