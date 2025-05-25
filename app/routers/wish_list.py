from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.wishlist import Wishlist
from app.routers.auth import get_current_user
from app.models.book import Book
from app.models.rating import Rating
from app.models.review import Review


router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.post("/")
def add_to_wishlist(book_name: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    book = db.query(Book).filter(Book.title == book_name).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Provjera postoji li rating za korisnika i tu knjigu
    rating_exists = db.query(Rating).filter_by(user_id=current_user.id, book_id=book.id).first()
    if rating_exists:
        raise HTTPException(status_code=400, detail="Cannot add book to wishlist because it is already rated")

    # Provjera postoji li review za korisnika i tu knjigu
    review_exists = db.query(Review).filter_by(user_id=current_user.id, book_id=book.id).first()
    if review_exists:
        raise HTTPException(status_code=400, detail="Cannot add book to wishlist because it is already reviewed")

    already_in_wishlist = db.query(Wishlist).filter_by(user_id=current_user.id, book_id=book.id).first()
    if already_in_wishlist:
        raise HTTPException(status_code=400, detail="Book already in wishlist")

    wishlist_item = Wishlist(user_id=current_user.id, book_id=book.id)
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)

    return {"message": "Book added to wishlist", "wishlist_id": wishlist_item.id}

@router.delete("/{book_id}")
def remove_from_wishlist(book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    wishlist_item = db.query(Wishlist).filter_by(user_id=current_user.id, book_id=book_id).first()
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Book not found in wishlist")

    db.delete(wishlist_item)
    db.commit()
    return {"message": "Book removed from wishlist"}
@router.get("/")
def get_wishlist(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    wishlist_entries = db.query(Wishlist).filter_by(user_id=current_user.id).all()

    result = []
    for entry in wishlist_entries:
        book = db.query(Book).filter_by(id=entry.book_id).first()
        if book:
            result.append({
                "book_id": book.id,
                "title": book.title,
                "author": book.author
            })

    return result
