from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from database import get_db
from schemas import ProgressResponse, ReviewRequest, CardResponse, ProgressBase
from crud import crud_progress, crud_flashcard
from .auth import get_current_user
from services.srs_algorithm import calculate_sm2

router = APIRouter()

@router.get("/due-progress", response_model=List[ProgressResponse], summary="Retrieves progress data for the cards you need to work on today")
def get_due_reviews(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud_progress.get_due_cards_for_user(db, user_id=current_user.id)

@router.get("/library", response_model=List[ProgressResponse] ,summary="Retrieves progress data for all of the user's cards")
def get_library(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud_progress.get_all_progress_for_user(db, user_id=current_user.id)

@router.get("/due", response_model=List[CardResponse], summary="Retrieves cards you need to work on today")
def get_due_cards_with_details(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud_progress.get_due_flashcards_for_user(db, user_id=current_user.id)

@router.put("", response_model=ProgressResponse, summary="Submits a review for a card and updates the progress")
def submit_review(review: ReviewRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    card_id = review.card_id
    # Card availability check
    card = crud_flashcard.get_flashcard(db, card_id)
    if not card:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Flashcard not found")

    progress = crud_progress.get_progress(db, current_user.id, card_id)
    
    if progress:
        iterations = progress.iterations
        interval = progress.interval
        ease_factor = progress.ease_factor
        next_review_date = progress.next_review_date
    else:
        iterations = 0
        interval = 1
        ease_factor = 2.5
        next_review_date = None
        
    new_iter, new_interval, new_ease, card_status, next_date = calculate_sm2(
        grade=review.grade,
        iterations=iterations,
        interval=interval,
        ease_factor=ease_factor,
        next_review_date=next_review_date
    )

    new_data = ProgressBase(
        iterations=new_iter,
        interval=new_interval,
        ease_factor=new_ease,
        status=card_status,
        next_review_date=next_date,
        last_reviewed_at=datetime.now(timezone.utc)
    )
    
    return crud_progress.create_or_update_progress(db, current_user.id, card_id, new_data)

@router.get("/progress/{card_id}", response_model=ProgressResponse, summary="Retrieves progress data for a specific card")
def get_card_progress(card_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    progress = crud_progress.get_progress(db, current_user.id, card_id)
    if not progress:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="You haven't studied this card yet.")
    return progress
