from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models.progress import CardProgress
from schemas.progress_schema import ProgressBase

def get_progress(db: Session, user_id: int, card_id: int):
    return db.query(CardProgress).filter(CardProgress.user_id == user_id, CardProgress.card_id == card_id).first()

def get_due_cards_for_user(db: Session, user_id: int):
    return db.query(CardProgress).filter(
        CardProgress.user_id == user_id,
        CardProgress.next_review_date <= datetime.now(timezone.utc),
        CardProgress.status != "mastered"
    ).all()

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
