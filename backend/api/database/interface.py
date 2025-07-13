from __future__ import annotations
import abc
import typing
from typing import overload, AsyncGenerator, Callable, Literal


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.api.database import PostgresImplementation
    from backend.api.database import MongoImplementation
ABC_TYPE = Callable[..., AsyncGenerator["DatabaseInterface"]]
PG_TYPE = Callable[..., AsyncGenerator["PostgresImplementation"]]
MONGO_TYPE = Callable[..., AsyncGenerator["MongoImplementation"]]
MOCK_TYPE = Callable[..., AsyncGenerator["MockImplementation"]]


class DatabaseInterface(abc.ABC):
    database_name: str
    session_factory = None
    _registry: dict[str, typing.Type["DatabaseInterface"]] = {}
    """This is ABC class with registry pattern implementation.
    To use in code:
    `DatabaseInterface["SQL"].add_record(record="test")` 
    `DatabaseInterface["Mongo"].add_record(record="test")`
    """

    def __init_subclass__(cls, *args, **kwargs):
        if "database_name" not in cls.__dict__:
            raise NotImplementedError("'database_name' field not defined in subclass")
        if "session_factory" not in cls.__dict__:
            raise NotImplementedError("'session_factory' field not defined in subclass")
        cls._registry[cls.database_name.lower()] = cls

    @abc.abstractmethod
    def __init__(self, *args, session, **kwargs):
        "make db client required at class writing"

    @staticmethod
    @overload
    def get_db_impl(*, db_name: Literal["Postgres"]) -> PG_TYPE: ...

    @staticmethod
    @overload
    def get_db_impl(*, db_name: Literal["Mongo"]) -> MONGO_TYPE: ...

    @staticmethod
    @overload
    def get_db_impl(*, db_name: Literal["Mock"]) -> MOCK_TYPE: ...

    @classmethod
    def get_db_impl(cls, *, db_name: str) -> ABC_TYPE:
        async def get_db() -> AsyncGenerator[DatabaseInterface, None]:
            db = cls._registry[db_name.lower()]
            async with db.session_factory as session:
                yield db(session=session)

        return get_db

    # @classmethod
    # def get_db_impl(cls, *, db_name: str):
    #     async def _get_db_impl() -> typing.Type[DatabaseInterface]:
    #         db = cls._registry[db_name.lower()]
    #         async with db.session_factory as session:
    #             yield db(session=session)
    #
    #     return _get_db_impl

    @abc.abstractmethod
    def get_record(self):
        pass

    @abc.abstractmethod
    def get_many_records(self) -> list:
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """

    @abc.abstractmethod
    def add_record(self, record: typing.Any):
        pass

    @abc.abstractmethod
    def add_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """

    @abc.abstractmethod
    def update_record(self, record: typing.Any):
        pass

    @abc.abstractmethod
    def update_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """

    @abc.abstractmethod
    def delete_record(self, record: typing.Any):
        pass

    @abc.abstractmethod
    def delete_many_records(self, records: typing.List[typing.Any]):
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
