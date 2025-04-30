from fastapi import APIRouter, HTTPException, Path
from models.book import Book
from models.review import Review
from data.books import books
from typing import Annotated

router = APIRouter(prefix="/books")


@router.get("/")
def get_all_books(
        sort: bool = False
) -> list[Book]:
    """Returns the list of available books."""
    if sort:
        return sorted(books.values(), key=lambda book: book.review)
    else:
        return list(books.values())


@router.post("/")
def add_book(book: Book):
    """Adds a new book."""
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book ID already exists.")
    books[book.id] = book
    return "Book successfully added."


@router.delete("/")
def delete_all_books():
    """Deletes all books."""
    books.clear()
    return "All books successfully deleted"


@router.delete("/{id}")
def delete_book(
        id: Annotated[int, Path(description="The ID of the book to delete")]
):
    """Deletes the book with the given ID."""
    try:
        del books[id]
        return "Book successfully deleted"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.get("/{id}")
def get_book_by_id(
        id: Annotated[int, Path(description="The ID of the book to get")]
) -> Book:
    """Returns the book with the given id."""
    try:
        return books[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.post("/{id}/review")
def add_review(
        id: Annotated[int, Path(description="The ID of the book to which add the review")],
        review: Review
):
    """Adds a review to the book with the given ID."""
    try:
        books[id].review = review.review
        return "Review successfully added"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.put("/{id}")
def update_book(
        id: Annotated[int, Path(description="The ID of the book to update")],
        book: Book
):
    """Updates the book with the given ID."""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[id] = book
    return "Book successfully updated"
