import os

import pydantic


class Database(pydantic.BaseModel):
    user: str | None = None  # Made optional for SQLite
    password: str | None = None  # Made optional for SQLite
    hostname: str | None = None  # Made optional for SQLite
    port: int | None = None  # Made optional for SQLite
    db_name: str
    sync_driver: str
    async_driver: str

    @pydantic.computed_field
    @property
    def sync_conn_string(self) -> str:
        """Generate a database connection string based on the driver."""
        if self.sync_driver.startswith("sqlite"):
            return f"{self.sync_driver}:///{self.db_name}"
        else:
            return (
                f"{self.sync_driver}://{self.user}:{self.password}@"
                f"{self.hostname}:{self.port}/{self.db_name}"
            )

    @pydantic.computed_field
    @property
    def async_conn_string(self) -> str:
        """Generate a database connection string based on the driver."""
        if self.async_driver.startswith("sqlite"):
            return f"{self.async_driver}:///{self.db_name}"
        else:
            return (
                f"{self.async_driver}://{self.user}:{self.password}@"
                f"{self.hostname}:{self.port}/{self.db_name}"
            )


databases: dict[str, Database] = {
    "sqlite": Database(
        db_name="sqlite_db",
        sync_driver="sqlite",
        async_driver="sqlite+aiosqlite",
    ),
    "postgres": Database(
        user=os.getenv("POSTGRES_USER") or "postgres",
        password=os.getenv("POSTGRES_PASSWORD") or "postgres",
        hostname=os.getenv("POSTGRES_HOSTNAME") or "localhost",
        port=os.getenv("POSTGRES_PORT") or 5432,
        db_name=os.getenv("POSTGRES_DB") or "LogsObsDb",
        sync_driver="postgresql+psycopg2",
        async_driver="postgresql+asyncpg",
    ),
    "mongo": Database(
        user=os.getenv("MONGO_USER") or "mongo",
        password=os.getenv("MONGO_PASSWORD") or "mongo",
        hostname=os.getenv("MONGO_HOSTNAME") or "localhost",
        port=os.getenv("MONGO_PORT") or 27017,
        db_name=os.getenv("MONGO_DB") or "LogsPoC",
        sync_driver="mongodb",  # no real use for sync in MongoDB client
        async_driver="mongodb+motor",  # or just "mongodb" if using `motor`
    ),
}
