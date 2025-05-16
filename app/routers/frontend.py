from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.db import SessionDep
from sqlmodel import select
from models.book import Book


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    text = {
        "title": "Welcome to the library",
        "content": "Have you ever seen this place?"
    }
    return templates.TemplateResponse(
        request=request, name="home.html",
        context={"text": text}
    )

@router.get("/book_list", response_class=HTMLResponse)
def show_book_list(request: Request, session: SessionDep):
    statement = select(Book)
    books = session.exec(statement).all()
    context = {"books": books}
    return templates.TemplateResponse(
        request=request, name="list.html", context=context
    )


@router.get("/add_book", response_class=HTMLResponse)
def add_book_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="add.html"
    )
