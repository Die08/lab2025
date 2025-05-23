from fastapi import APIRouter
from app.data.db import SessionDep
from sqlmodel import select
from app.models.user import User, UserPublic
from app.models.book import Book, BookPublic
from app.models.book_user_link import BookUserLink

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns all users"""
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.get("/{id}/books")
def get_user_books(
        id: int,
        session: SessionDep
) -> list[BookPublic]:
    """Returns all the books held by the given user."""
    statement = select(Book).join(BookUserLink).where(BookUserLink.user_id == id)  # NOQA
    result = session.exec(statement).all()
    return result
