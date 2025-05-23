from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.data.db import SessionDep
from sqlmodel import select
from app.models.book import Book


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    text = {
        "title": "Welcome to the library",
        "content": "Have you ever seen this place?"
    }
    return templates.TemplateResponse(
        #renderizza il file home.html, passando il contesto { "text": text }.
        #Nel template potrai fare {{ text.title }} e {{ text.content }}.
        request=request, name="home.html",
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
async def add_book_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="add.html"
    )
#Ritorna semplicemente il form HTML definito in add.html, che invia i dati (via POST) all’endpoint API di creazione (add_book_from_form).

