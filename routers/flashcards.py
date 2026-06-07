from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import flashcard_schema
from crud import crud_flashcard
from .auth import get_current_user
from models.user import User
from services.pexels_client import get_image_for_word

router = APIRouter()

@router.get("/public", response_model=List[flashcard_schema.FlashcardResponse])
def read_public_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Misafir kullanıcılar da erişebilir."""
    cards = crud_flashcard.get_public_flashcards(db, skip=skip, limit=limit)
    return cards

@router.get("/", response_model=List[flashcard_schema.FlashcardResponse])
def read_user_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cards = crud_flashcard.get_user_flashcards(db, user_id=current_user.id, skip=skip, limit=limit)
    return cards

@router.post("/", response_model=flashcard_schema.FlashcardResponse)
async def create_card(card: flashcard_schema.FlashcardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Kullanıcı görsel URL göndermediyse otomatik çek
    image_url = card.image_url
    if not image_url:
        image_url = await get_image_for_word(card.word)
    
    # Kartı oluştur
    db_card = crud_flashcard.create_flashcard(db=db, flashcard=card, user_id=current_user.id, image_url=image_url)
    return db_card

@router.get("/preview-image")
async def preview_image(word: str, current_user: User = Depends(get_current_user)):
    image_url = await get_image_for_word(word)
    return {"image_url": image_url}

@router.patch("/{card_id}", response_model=flashcard_schema.FlashcardResponse)
def update_card(card_id: int, card_update: flashcard_schema.FlashcardUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_card = crud_flashcard.get_flashcard(db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    if db_card.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this card")
    
    return crud_flashcard.update_flashcard(db=db, db_flashcard=db_card, updates=card_update)

@router.delete("/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_card = crud_flashcard.get_flashcard(db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    if db_card.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this card")
    
    crud_flashcard.delete_flashcard(db=db, db_flashcard=db_card)
    return {"message": "Flashcard deleted successfully"}
