from sqlmodel import SQLModel, Field


class BookUserLink(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
