from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class CardProgress(Base):
    __tablename__ = "card_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("flashcards.id"))
    iterations = Column(Integer, default=0)
    interval = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    status = Column(String, default="learning")
    next_review_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="progress")
    card = relationship("Flashcard", back_populates="progress")
