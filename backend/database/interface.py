from __future__ import annotations

import abc
import typing
from collections.abc import AsyncGenerator, Callable
from typing import ClassVar, Literal, overload
from sqlmodel import SQLModel

import fastapi
import pydantic

if typing.TYPE_CHECKING:
    from backend.database import (
        MockImplementation,
        MongoImplementation,
        PostgresImplementation,
        FileStorageImplementation,
    )

    _ = PostgresImplementation
    _ = MongoImplementation
    _ = MockImplementation
    _ = FileStorageImplementation


ABC_TYPE = Callable[..., AsyncGenerator["DatabaseInterface"]]
PG_TYPE = Callable[..., AsyncGenerator["PostgresImplementation"]]
MONGO_TYPE = Callable[..., AsyncGenerator["MongoImplementation"]]
MOCK_TYPE = Callable[..., AsyncGenerator["MockImplementation"]]
FS_TYPE = Callable[..., AsyncGenerator["FileStorageImplementation"]]


class DatabaseInterface(abc.ABC):
    database_name: str
    session_factory = None
    _registry: ClassVar[dict[str, type[DatabaseInterface]]] = {}
    sessions = {}
    """This is ABC class with registry pattern implementation.
    To use in code:
    `DatabaseInterface["SQL"].add_record(record="test")`
    `DatabaseInterface["Mongo"].add_record(record="test")`
    """

    def __init_subclass__(cls, *args, **kwargs):
        msg: str = "field not defined in subclass"
        if "database_name" not in cls.__dict__:
            raise NotImplementedError(f"'database_name' {msg}")
        if "session_factory" not in cls.__dict__:
            raise NotImplementedError(f"'session_factory' {msg}")
        cls._registry[cls.database_name.lower()] = cls
        cls.init_db()
        cls.sessions[cls.database_name.lower()] = typing.Annotated[
            f"{cls.database_name}Implementation",
            fastapi.Depends(
                DatabaseInterface.get_db_impl(db_name=cls.database_name)
            ),
        ]

    @abc.abstractmethod
    def __init__(self, *args, session, **kwargs) -> None:
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

    @staticmethod
    @overload
    def get_db_impl(*, db_name: Literal["FileStorage"]) -> FS_TYPE: ...

    @classmethod
    def get_db_impl(cls, *, db_name: str) -> ABC_TYPE:
        async def get_db() -> AsyncGenerator[DatabaseInterface]:
            db = cls._registry[db_name.lower()]
            async with db.session_factory() as session:
                yield db(session=session)

        return get_db

    @classmethod
    def get_session(cls, *, db_name: str) -> ABC_TYPE:
        return cls.sessions[db_name.lower()]

    @classmethod
    def init_db(cls):
        """
        Initialize database:
        - Create all tables/collections defined if they don't exist.
        - If not applicable don't create implementation for init_db.
        """
        pass

    @abc.abstractmethod
    def get_record(
        self,
        key: str,
        value: str,
        place: typing.Any = None,
    ) -> SQLModel | False:
        pass

    @abc.abstractmethod
    def get_many_records(
        self,
        records: typing.Any,
        table: typing.Any = None,
    ) -> list:
        """Need to be separate from get_record.
        Some databases offer bulk operations.
        If db supports bulk get, please implement.
        If db doesn't support bulk get, please implement for loop get_record.
        Function name contains 'many' due to similarities with get_record.
        There is a risk of mistake while function call.
        """

    @abc.abstractmethod
    def list_records(
        self,
        start: int,
        size: int,
    ) -> typing.List[typing.Any]:
        """Implement function that returns all available records.
        Implement simple pagination with start pointer and size.
        """
        pass

    @abc.abstractmethod
    def add_record(
        self,
        body: typing.Any,
        place: typing.Any,
    ) -> SQLModel | False:
        pass

    @abc.abstractmethod
    def add_many_records(
        self,
        records: list[typing.Any],
    ):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """

    @abc.abstractmethod
    def update_record(
        self,
        record: typing.Any,
    ):
        pass

    @abc.abstractmethod
    def update_many_records(
        self,
        records: list[typing.Any],
    ):
        """Need to be separate from add_record.
        Some databases offer bulk operations.
        If db supports bulk add, please implement.
        If db doesn't support bulk add, please implement for loop add_record.
        Function name contains 'many' due to similarities with add_record.
        There is a risk of mistake while function call.
        """

    @abc.abstractmethod
    def delete_record(
        self,
        record: typing.Any,
    ):
        pass

    @abc.abstractmethod
    def delete_many_records(
        self,
        records: list[typing.Any],
    ):
        """Need to be separate from delete_record.
        Some databases offer bulk operations.
        If db supports bulk delete, please implement.
        If db doesn't support bulk delete, please add for loop delete_record.
        Function name contains 'many' due to similarities with delete_record.
        There is a risk of mistake while function call.
        """
