from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review
from app.models.book import Book
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/")
def create_review(
    content: str,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db_review = Review(content=content, user_id=current_user.id, book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return {
        "message": "Review added successfully",
        "review_id": db_review.id,
        "user_id": current_user.id  
    }

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter_by(id=review_id, user_id=current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

@router.get("/me")
def get_my_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reviews = db.query(Review).filter(Review.user_id == current_user.id).all()
    return [
        {
            "review_id": r.id,
            "book_id": r.book_id,
            "content": r.content
        }
        for r in reviews
    ]

@router.put("/{review_id}")
def update_review(review_id: int, content: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.content = content
    db.commit()
    db.refresh(review)

    return {"message": "Review updated successfully", "review": {
        "id": review.id,
        "content": review.content
    }}