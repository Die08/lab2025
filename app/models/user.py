from datetime import date
from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    name: str
    city: str


class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserPublic(BaseUser):
    pass


