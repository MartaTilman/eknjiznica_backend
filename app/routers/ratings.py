from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rating import Rating
from app.models.reading_list import ReadingList
from app.routers.auth import get_current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/")
def add_rating(score: int, book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    
    db_rating = Rating(score=score, user_id=current_user.id, book_id=book_id)
    db.add(db_rating)

   
    exists = db.query(ReadingList).filter_by(user_id=current_user.id, book_id=book_id).first()
    if not exists:
        reading_item = ReadingList(user_id=current_user.id, book_id=book_id)
        db.add(reading_item)

    db.commit()
    db.refresh(db_rating)
    return {"message": "Rating added successfully", "rating_id": db_rating.id}
