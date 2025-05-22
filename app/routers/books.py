'''modulo che definisce tutti gli endpoint FastAPI per la gestione delle risorse “Book”'''
from fastapi import APIRouter, HTTPException, Path, Form
#FastAPI: APIRouter per raggruppare gli endpoint, HTTPException per gestire errori HTTP,
# Path e Form per parametrizzare path e form data.
from app.models.review import Review
from typing import Annotated
from app.models.book import Book, BookPublic, BookCreate
#Modelli: Review (schema Pydantic per validazione del voto), Book, BookPublic,
# BookCreate (modelli SQLModel/Pydantic definiti in book.py).
from app.data.db import SessionDep
#Database: SessionDep, una dipendenza che fornisce la sessione di connessione.
from sqlmodel import select, delete
#Select: funzione di utilità per interrogazioni SQLModel.

router = APIRouter(prefix="/books")
#Questo fa sì che tutte le rotte definite abbiano URL che iniziano con /books

@router.get("/")
def get_all_books(
        session: SessionDep, #iniettata automaticamente tramite la dependency SessionDep
        sort: bool = False #flag facoltativo (default False); se True, ordina i libri in base al voto (review).
) -> list[BookPublic]: # lista di istanze BookPublic (includono id, title, author, review) books.
    """Returns the list of available books."""
    statement = select(Book)
    books = session.exec(statement).all()
    if sort:
        return sorted(books, key=lambda book: book.review)
    else:
        return books


@router.post("/")
def add_book(book: BookCreate, session: SessionDep):
    #nput: JSON conforme allo schema BookCreate (campi title, author, review con validazione 1–5
    """Adds a new book."""
    validated_book = Book.model_validate(book) #model_validate trasforma e convalida il Pydantic model in un’istanza Book.
    session.add(validated_book)
    session.commit()
    return "Book successfully added."


@router.post("_form/")
#rispetto a add_book: i dati del libro arrivano da un form HTML anziché da JSON.
def add_book_from_form(
        book: Annotated[BookCreate, Form()], #legge campi title, author, review inviati come form-url-encoded.
        session: SessionDep,
):
    """Adds a new book"""
    validated_book = Book.model_validate(book)
    session.add(validated_book)
    session.commit()
    return "Book successfully added."


@router.delete("/")
def delete_all_books(session: SessionDep):
    """Deletes all books."""
    statement = delete(Book)
    session.exec(statement)
    session.commit()
    return "All books successfully deleted"


@router.delete("/{id}")
def delete_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to delete")] #id: estratto dall’URL, validato come int
):
    """Deletes the book with the given ID."""
    book = session.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return "Book successfully deleted"


@router.get("/{id}")
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to get")]
) -> BookPublic:
    """Returns the book with the given id."""
    book = session.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/{id}/review")
def add_review(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to which add the review")],
        review: Review
):
    """Adds a review to the book with the given ID."""
    book = session.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.review = review.review
    session.add(book)
    session.commit()
    return "Review successfully added"


@router.put("/{id}")
def update_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to update")],
        new_book: BookCreate
):
    """Updates the book with the given ID."""
    book = session.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = new_book.title
    book.author = new_book.author
    book.review = new_book.review
    session.commit()
    return "Book successfully updated"
