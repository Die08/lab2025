from fastapi import APIRouter, Request
#APIRouter: crea un router modulare, per raggruppare insieme rotte “frontend” distinte da quelle API REST pure.
#Request: oggetto che incapsula la richiesta HTTP; serve a Jinja2Templates per generare la risposta.
from fastapi.responses import HTMLResponse
#HTMLResponse: specifica che la risposta sarà HTML (e non JSON di default).
from fastapi.templating import Jinja2Templates
#Jinja2Templates: motore di template Jinja2 integrato in FastAPI, consente di caricare e renderizzare file .html.
from app.data.db import SessionDep
#SessionDep: dependency che fornisce una sessione di database (importata da data/db.py).
from sqlmodel import select
#select: helper di SQLModel per costruire query.
from app.models.book import Book
#Book: modello SQLModel che rappresenta la tabella dei libri.


templates = Jinja2Templates(directory="app/templates") # cartella in cui Jinja2 cercherà i file .html
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
#mappa la radice del sito (/) e imposta il tipo di risposta su HTML.
def home(request: Request):
    text = { #dizionario con chiavi title e content, usato nel template.
        "title": "Welcome to the library",
        "content": "Have you ever seen this place?"
    }
    return templates.TemplateResponse(
        #renderizza il file home.html, passando il contesto { "text": text }.
        #Nel template potrai fare {{ text.title }} e {{ text.content }}.
        # request=request, name="home.html",
        context={"text": text}
    )

@router.get("/book_list", response_class=HTMLResponse)
def show_book_list(request: Request, session: SessionDep): #session: SessionDep: ottiene una sessione aperta sul database.
    statement = select(Book) #costruisce una query per recuperare tutti i record della tabella Book.
    books = session.exec(statement).all()  #esegue la query e ritorna la lista di oggetti Book.
    context = {"books": books} #passa l’elenco al template list.html, dove con un ciclo {% for book in books %}
    # verranno visualizzate righe di tabella con book.id, book.title, book.author, book.review.
    return templates.TemplateResponse(
        request=request, name="list.html", context=context
    )


@router.get("/add_book", response_class=HTMLResponse)
def add_book_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="add.html"
    )
#Ritorna semplicemente il form HTML definito in add.html, che invia i dati (via POST) all’endpoint API di creazione (add_book_from_form).

