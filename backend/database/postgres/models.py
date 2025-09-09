from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    email: str = Field(index=True)

    workspaces: list["Workspace"] = Relationship(
        back_populates="owner",
        cascade_delete=True,  # for python cascade delete
    )
    files: List["File"] = Relationship(
        back_populates="owner",
        cascade_delete=True,  # for python cascade delete
    )


class Workspace(SQLModel, table=True):
    __tablename__ = "workspaces"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    owner: Optional[User] = Relationship(back_populates="workspaces")


class File(SQLModel, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str
    size_mb: float
    type: str

    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    owner: Optional[User] = Relationship(back_populates="files")


tables: dict[str, type[SQLModel]] = {
    "users": User,
    "workspaces": Workspace,
    "files": File,
}

if __name__ == "__main__":
    # need to comment out postgres implementation in init
    from backend.database.config import pg_config
    from sqlmodel import Session, create_engine

    # Create a sync engine
    engine = create_engine(pg_config.sync_url)

    # Create tables if not already created
    SQLModel.metadata.create_all(engine, checkfirst=True)

    # Populate data
    with Session(engine) as session:
        for u in range(1, 11):
            user = User(
                user_id=f"user_{u}",
                name=f"User {u}",
                email=f"user{u}@example.com",
            )

            # Add workspaces
            for w in range(1, 11):
                workspace = Workspace(
                    name=f"Workspace {w} of user {u}",
                    owner=user,
                )
                session.add(workspace)

            # Add files
            for f in range(1, 11):
                file = File(
                    name=f"File {f} of user {u}",
                    url=f"https://example.com/user{u}/file{f}.txt",
                    size_mb=10 * f,
                    type="txt",
                    owner=user,
                )
                session.add(file)

            # Add the user last so foreign keys are consistent
            session.add(user)

        # Commit all changes
        session.commit()
