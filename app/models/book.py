'''Il file book.py definisce i modelli di dati per la risorsa “Book” utilizzando SQLModel,
 che unisce le potenzialità di SQLAlchemy (mappatura object-relational) e Pydantic (validazione e serializzazione).'''
from sqlmodel import SQLModel, Field
from typing import Annotated
'''QLModel è la classe base da cui ereditano tutti i modelli:
 fornisce sia il mapping verso il database sia la validazione dei dati.
Field serve a specificare dettagli aggiuntivi sui campi (es. vincoli, chiavi).
Annotated (da typing) permette di combinare il tipo Python 
con metadati (qui usato per la validazione Pydantic) .'''

class BookBase(SQLModel):
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)]


class Book(BookBase, table=True): #table=True indica a SQLModel di creare una tabella corrispondente chiamata per convenzione “book”.
    id: int = Field(default=None, primary_key=True) #Il campo id è dichiarato intero, con primary_key=True
    # per marcare la chiave primaria; default=None permette al database di assegnare automaticamente un valore (autoincrement)

class BookCreate(BookBase):
    pass
#Viene usato come schema d’ingresso (request body) nelle API quando si crea un nuovo libro;
# Pydantic controllerà la presenza e la validità dei campi definiti in BookBase bookbook


class BookPublic(BookBase):
    id: int
#Estende BookBase aggiungendo il campo id.
#Viene impiegato come schema d’uscita (response model) alle API, garantendo che il client riceva anche
# l’identificativo assegnato dal database

'''BookBase: definisce gli attributi comuni e la logica di validazione.
Book: mappa la tabella vera e propria, con chiave primaria.
BookCreate e BookPublic: differenziano gli schemi in ingresso (create) e in uscita (public), 
garantendo una chiara separazione dei modelli di dominio nei diversi contesti.'''