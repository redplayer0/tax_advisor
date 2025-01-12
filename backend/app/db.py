from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)


class UserPublic(UserBase):
    username: str


class UserCreate(UserBase):
    password: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# Code below omitted 👇
