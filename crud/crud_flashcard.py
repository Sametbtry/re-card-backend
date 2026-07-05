from sqlalchemy.orm import Session
from models import Flashcard
from schemas import CardBase, CardUpdate

def get_flashcard(db: Session, card_id: int):
    return db.query(Flashcard).filter(Flashcard.id == card_id).first()

def get_public_flashcards(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(Flashcard).filter(Flashcard.is_public == True).order_by(Flashcard.id.desc())
    total = query.count()
    cards = query.offset(skip).limit(limit).all()
    return cards, total

def get_user_flashcards(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    query = db.query(Flashcard).filter(Flashcard.creator_id == user_id).order_by(Flashcard.id.desc())
    total = query.count()
    cards = query.offset(skip).limit(limit).all()
    return cards, total

def create_flashcard(db: Session, flashcard: CardBase, user_id: int):
    db_flashcard = Flashcard(
        **flashcard.model_dump(),
        creator_id=user_id
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def update_flashcard(db: Session, db_flashcard: Flashcard, updates: CardUpdate):
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flashcard, key, value)
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def delete_flashcard(db: Session, db_flashcard: Flashcard):
    db.delete(db_flashcard)
    db.commit()
