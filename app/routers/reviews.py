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
