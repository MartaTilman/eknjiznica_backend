from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
