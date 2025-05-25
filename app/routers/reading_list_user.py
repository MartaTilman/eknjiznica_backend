from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.book import Book
from app.models.rating import Rating
from app.models.review import Review
from app.models.reading_list import ReadingList
from app.routers.auth import get_current_user

router = APIRouter(prefix="/reading_list", tags=["reading_list"])

@router.get("/")
def get_full_reading_list(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = []
    added_book_ids = set()

    # 1. Knjige s recenzijom
    reviews = db.query(Review).filter(Review.user_id == current_user.id).all()
    for review in reviews:
        book = db.query(Book).filter(Book.id == review.book_id).first()
        if not book:
            continue
        rating = db.query(Rating).filter_by(user_id=current_user.id, book_id=book.id).first()
        result.append({
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "rating": rating.score if rating else None,
            "review": review.content
        })
        added_book_ids.add(book.id)

    # 2. Knjige s ocjenom ali bez recenzije
    ratings = db.query(Rating).filter(Rating.user_id == current_user.id).all()
    for rating in ratings:
        if rating.book_id in added_book_ids:
            continue
        book = db.query(Book).filter(Book.id == rating.book_id).first()
        if not book:
            continue
        result.append({
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "rating": rating.score,
            "review": None
        })
        added_book_ids.add(book.id)

    

    return result
