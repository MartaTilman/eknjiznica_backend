from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reading_list import ReadingList
from app.models.book import Book
from app.models.rating import Rating
from app.routers.auth import get_current_user
from app.models.review import Review 

router = APIRouter(prefix="/reading_list", tags=["reading_list"])

@router.get("/")
def get_reading_list(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    reading_list_entries = db.query(ReadingList).filter(ReadingList.user_id == current_user.id).all()

    result = []

    for entry in reading_list_entries:
        book = db.query(Book).filter(Book.id == entry.book_id).first()
        if not book:
            continue

        rating = db.query(Rating).filter(
            Rating.user_id == current_user.id,
            Rating.book_id == book.id
        ).first()

        review = db.query(Review).filter(
            Review.user_id == current_user.id,
            Review.book_id == book.id
        ).first()

        result.append({
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "rating": rating.score if rating else None,
            "review": review.content if review else None  
        })

    return result