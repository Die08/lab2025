from sqlmodel import SQLModel, Field
from datetime import datetime




class BaseUser(SQLModel): #classe base definiscce utente
    name: str
    birthdate: str
    city: str

class User(BaseUser, table=True):
    id: int| None = Field(default=None, primary_key=True)


class Bookpublic(BaseUser):
    pass


