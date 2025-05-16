from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from faker import Faker
import os
from models.book import Book


sqlite_file_name = "app/data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args,
                       echo=True)


def init_database():
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):
                book = Book(title=f.sentence(nb_words=5), author=f.name(),
                            review=f.pyint(1, 5))
                session.add(book)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
