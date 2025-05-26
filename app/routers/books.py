from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.book import Book
from app.models.review import Review
from app.models.rating import Rating
from app.models.user import User
from app.routers.auth import get_current_user

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

@router.get("/details_by_title/")
def get_book_details_by_title(title: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    book = db.query(Book).filter(Book.title == title).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    reviews = db.query(Review, User).join(User, Review.user_id == User.id).filter(Review.book_id == book.id).all()
    ratings = db.query(Rating, User).join(User, Rating.user_id == User.id).filter(Rating.book_id == book.id).all()

    return {
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
        },
        "reviews": [
            {
                "content": review.content,
                "user": user.username
            }
            for review, user in reviews
        ],
        "ratings": [
            {
                "score": rating.score,
                "user": user.username
            }
            for rating, user in ratings
        ]
    }
