from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}