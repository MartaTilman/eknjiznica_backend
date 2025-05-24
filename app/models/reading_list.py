from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class ReadingList(Base):
    __tablename__ = "reading_list"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

 
    user = relationship("User", back_populates="reading_list")
    book = relationship("Book", back_populates="reading_list")

    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='_user_book_uc'),)
