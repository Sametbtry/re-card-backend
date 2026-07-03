from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from database import get_db
from schemas import CardPaginatedResponse, CardResponse, CardBase, CardUpdate, ImageSearchResponse
from crud import crud_flashcard
from .auth import get_current_user
from services.pexels_client import get_image_for_word

router = APIRouter()

import math

@router.get("/public", response_model=CardPaginatedResponse, summary= "get public flashcards")
def read_public_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Misafir kullanıcılar da erişebilir."""
    cards, total = crud_flashcard.get_public_flashcards(db, skip=skip, limit=limit)
    total_pages = math.ceil(total / limit) if limit > 0 else 1
    return CardPaginatedResponse(
        items = cards,
        total = total,
        page = (skip // limit) + 1 if limit > 0 else 1,
        size = limit,
        total_pages = total_pages
    )

@router.get("/", response_model=CardPaginatedResponse, summary="get user's flashcards")
def read_user_cards(skip: int = 0, limit: int = 100, current_user = Depends(get_current_user), db : Session = Depends(get_db)):
    cards, total = crud_flashcard.get_user_flashcards(db, user_id=current_user.id, skip=skip, limit=limit)
    total_pages = math.ceil(total / limit) if limit > 0 else 1
    return CardPaginatedResponse(
        items = cards,
        total = total,
        page = (skip // limit) + 1 if limit > 0 else 1,
        size = limit,
        total_pages = total_pages
    )
        
@router.post("/", response_model=CardResponse, status_code= status.HTTP_201_CREATED, summary="Create a new flashcard")
async def create_card(card: CardBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # If the user hasn't submitted an image URL, fetch it automatically
    image_url = card.image_url
    if not image_url:
        image_url = await get_image_for_word(card.word)
    
    # crud function in the thread pool to avoid blocking the event loop.
    db_card = await run_in_threadpool(
        crud_flashcard.create_flashcard, db=db, flashcard=card, user_id=current_user.id, image_url=image_url
    )
    return db_card

@router.get("/images/search", response_model=ImageSearchResponse, summary="get card images url from pexels")
async def preview_image(word: str, current_user = Depends(get_current_user)):
    image_url = await get_image_for_word(word)
    return ImageSearchResponse(image_url= image_url)

@router.patch("/{card_id}", response_model=CardResponse, summary="Update a flashcard")
def update_card(card_id: int, card_update: CardUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_card = crud_flashcard.get_flashcard(db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Flashcard not found")
    if db_card.creator_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to update this card")

    updated_card = crud_flashcard.update_flashcard(db=db, db_flashcard=db_card, updates=card_update)
    return updated_card

@router.delete("/{card_id}", status_code= status.HTTP_204_NO_CONTENT, summary="Delete a flashcard")
def delete_card(card_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_card = crud_flashcard.get_flashcard(db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    if db_card.creator_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this card")
    
    crud_flashcard.delete_flashcard(db=db, db_flashcard=db_card)
    return Response(status_code= status.HTTP_204_NO_CONTENT)    
