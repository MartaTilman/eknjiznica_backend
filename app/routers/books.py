from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.book import Book

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_book(title: str, author: str, description: str, owner_id: int, db: Session = Depends(get_db)):
    book = Book(title=title, author=author, description=description, owner_id=owner_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()
