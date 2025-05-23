from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from faker import Faker
import os
from models.book import Book
from models.user import User
from models.book_user_link import BookUserLink


sqlite_file_name = "app/data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args,
                       echo=True)


def init_database():
    ds_exists = os.path.isfile(sqlite_file_name) #è un booleano che indica se database.db esiste già sul disco.
    SQLModel.metadata.create_all(engine) #crea tutte le tabelle definiti nel modello SQLModel.
    if not ds_exists:
        f = Faker("it_IT") #crea un oggetto Faker per generare dati fake.
        with Session(engine) as session:
            for i in range(10):
                book = Book(title=f.sentence(nb_words=5), author=f.name(),
                            review=f.pyint(1, 5))
                user = User(name=f.name(), birthdate=f.date_of_birth(), city=f.city())
                session.add(user)
            session.commit()
            for i in range(10):
                book = Book(title=f.sentence(nb_words=5), author=f.name(), # se il file non esisteva (not ds_exists), viene istanziato Faker("it_IT") per generare 10 record fittizi con titolo (sentence), autore (name) e voto recensione (pyint(1,5)),
                            review=f.pyint(1, 5),
                            user_id=f.pyint(1, 10))
                session.add(book)
            session.commit()
            for i in range(5):
                link = BookUserLink(book_id=f.pyint(1, 10),
                                    user_id=f.pyint(1, 10))
                session.add(link)
            session.commit() #aggiunti e infine salvati (commit()).


def get_session(): #definisce un generator-based dependency per FastAPI che crea una Session
    # collegata all’engine, la fornisce al path operation e la chiude automaticamente al termine.
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
#alias di tipo che combina Session con Depends(get_session), semplificando la dichiarazione delle dipendenze
# nei router FastAPI (ad es. def get_all_books(session: SessionDep)).
