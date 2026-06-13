from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models.progress import CardProgress
from schemas.progress_schema import ProgressBase
from models.flashcard import Flashcard

def get_progress(db: Session, user_id: int, card_id: int):
    return db.query(CardProgress).filter(CardProgress.user_id == user_id, CardProgress.card_id == card_id).first()

def get_due_cards_for_user(db: Session, user_id: int):
    return db.query(CardProgress).filter(
        CardProgress.user_id == user_id,
        CardProgress.next_review_date <= datetime.now(timezone.utc),
        CardProgress.status != "mastered"
    ).all()

def get_due_flashcards_for_user(db: Session, user_id: int):
    now = datetime.now(timezone.utc)
    
    query = db.query(Flashcard, CardProgress).outerjoin(
        CardProgress, (Flashcard.id == CardProgress.card_id) & (CardProgress.user_id == user_id)
    ).filter(
        Flashcard.creator_id == user_id
    ).filter(
        (CardProgress.id == None) | 
        ((CardProgress.next_review_date <= now) & (CardProgress.status != "mastered"))
    ).all()
    
    def sort_key(item):
        f, p = item
        is_overdue = p is not None and p.next_review_date is not None and p.next_review_date.date() < now.date()
        return is_overdue
        
    query.sort(key=sort_key)
    return [f for f, p in query]

def get_all_progress_for_user(db: Session, user_id: int):
    return db.query(CardProgress).filter(CardProgress.user_id == user_id).all()

def create_or_update_progress(db: Session, user_id: int, card_id: int, new_data: dict):
    progress = get_progress(db, user_id, card_id)
    if not progress:
        progress = CardProgress(user_id=user_id, card_id=card_id, **new_data)
        db.add(progress)
    else:
        for key, value in new_data.items():
            setattr(progress, key, value)
    db.commit()
    db.refresh(progress)
    return progress
