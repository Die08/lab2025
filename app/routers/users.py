from app.data.db import SessionDep
from sqlmodel import select
from app.models.user import User, Bookpublic
from app.models.book import Book, BookPublic
from app.models.book_user_link import BookUserLink

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(session: SessionDep) -> list[Bookpublic]: #serve per convertire un oggetto della classe user in uno di user public
    """Returns all users."""
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.get("/{id}/books")
def get_user_books(
        id: int,
        session: SessionDep
        ) -> list[Bookpublic]:
    """Returns the books help by the given user."""
    statement = select(BookUserLink).join(BookUserLink).where(BookUser_id == id) # NOQA
    result = session.exec(statement).all()
    return result

