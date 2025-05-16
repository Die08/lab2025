from sqlmodel import SQLModel, Field
from typing import Annotated


class BookBase(SQLModel):
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)]


class Book(BookBase, table=True):
    id: int = Field(default=None, primary_key=True)


class BookCreate(BookBase):
    pass


class BookPublic(BookBase):
    id: int
