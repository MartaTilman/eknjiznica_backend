from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))


    reading_list = relationship("ReadingList", back_populates="book", cascade="all, delete-orphan")
