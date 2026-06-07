from sqlalchemy.orm import Session
from models.flashcard import Flashcard
from schemas.flashcard_schema import FlashcardCreate, FlashcardUpdate

def get_flashcard(db: Session, card_id: int):
    return db.query(Flashcard).filter(Flashcard.id == card_id).first()

def get_public_flashcards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Flashcard).filter(Flashcard.is_public == True).offset(skip).limit(limit).all()

def get_user_flashcards(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Flashcard).filter(Flashcard.creator_id == user_id).offset(skip).limit(limit).all()

def create_flashcard(db: Session, flashcard: FlashcardCreate, user_id: int, image_url: str | None = None):
    db_flashcard = Flashcard(
        **flashcard.model_dump(exclude={'image_url'}),
        creator_id=user_id,
        image_url=image_url
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def update_flashcard(db: Session, db_flashcard: Flashcard, updates: FlashcardUpdate):
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
