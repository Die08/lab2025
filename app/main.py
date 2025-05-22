from fastapi import FastAPI
#FastAPI: classe principale per creare l’applicazione.
from routers import books, frontend
#routers.books e routers.frontend: moduli in cui hai definito tutti gli endpoint API (/books)
# e le rotte di rendering dei template Jinja2.
from fastapi.staticfiles import StaticFiles
#StaticFiles: helper di FastAPI per montare e servire file statici (CSS, immagini, AVIF, ecc.).
from data.db import init_database
#init_database: funzione che crea le tabelle SQLModel e popola il database con dati finti se non esiste ancora
from contextlib import asynccontextmanager
#asynccontextmanager: dal modulo standard contextlib,
# serve a definire un “lifespan” asincrono in FastAPI, per eseguire del codice all’avvio e alla chiusura dell’app.


@asynccontextmanager # trasforma la funzione in un context manager asincrono.
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close
#Prima del yield (on start): viene chiamata init_database(), assicurando che al primo avvio:
#Vengano create tutte le tabelle SQLModel (tramite SQLModel.metadata.create_all)
#Se il DB non esisteva, vengano inseriti 10 record “fake” nella tabella Book


app = FastAPI(lifespan=lifespan)
#Passando il parametro lifespan=lifespan, FastAPI sa di dover eseguire il context manager definito sopra all’avvio e alla chiusura.
app.include_router(books.router, tags=["books"])
#books.router: tutti gli endpoint CRUD (/books, /books/{id}, /books/{id}/review, ecc.).
# Viene anche taggato con "books" per raggrupparli nella documentazione Swagger/OpenAPI.
app.include_router(frontend.router)
#frontend.router: rotte che servono pagine HTML (/, /book_list, /add_book).
# Non usa tag, così non compare nella sezione API docs come risorsa “books”
app.include_router(frontend.router, tags=["users"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")
#Rende disponibili i file presenti in app/static (es. styles.css, biblio.avif) all’URL /static/..

if __name__ == "__main__":
    # TODO: if you launch the application from here, you must modify the
    #  relative path to the static folder (in this file) from "app/static" to
    #  "static" and the relative path to the templates folder (in
    #  routers/frontend.py file) from "app/templates" to "templates".
    import uvicorn
    uvicorn.run("main:app", reload=True) # avvia il server ASGI con hot-reload (utile in sviluppo).
