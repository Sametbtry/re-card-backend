from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    word = Column(String, nullable=False, index=True)
    example_sentence = Column(Text, nullable=True)
    example_translation = Column(Text, nullable=True)
    translation = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("User", back_populates="flashcards")
    progress = relationship("CardProgress", back_populates="card", cascade="all, delete-orphan")
