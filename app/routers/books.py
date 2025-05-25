from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.book import Book
from app.routers.auth import get_current_user  
from app.models.user import User


router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_book(
    title: str,
    author: str,
    description: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    book = Book(
        title=title,
        author=author,
        description=description,
        owner_id=current_user.id  
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "owner_id": book.owner_id
    }

@router.get("/")
def get_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    return db.query(Book).all()
