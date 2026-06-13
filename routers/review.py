from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from database import get_db
from schemas import progress_schema
from crud import crud_progress, crud_flashcard
from .auth import get_current_user
from models.user import User
from services.srs_algorithm import calculate_sm2
from schemas import flashcard_schema

router = APIRouter()

@router.get("/", response_model=List[progress_schema.ProgressResponse])
def get_due_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Çalışılması gereken (next_review_date <= NOW) kartları getirir."""
    return crud_progress.get_due_cards_for_user(db, user_id=current_user.id)

@router.get("/library", response_model=List[progress_schema.ProgressResponse])
def get_library(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Kullanıcının öğrenmiş olduğu veya öğrenmekte olduğu tüm kartların durumunu getirir."""
    return crud_progress.get_all_progress_for_user(db, user_id=current_user.id)

@router.get("/due_cards", response_model=List[flashcard_schema.FlashcardResponse])
def get_due_cards_with_details(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Bugün çalışılması gereken kartları detaylarıyla birlikte (Flashcard) getirir."""
    return crud_progress.get_due_flashcards_for_user(db, user_id=current_user.id)

@router.post("/{card_id}", response_model=progress_schema.ProgressResponse)
def submit_review(card_id: int, review: progress_schema.ReviewRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Kart var mı kontrolü
    card = crud_flashcard.get_flashcard(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")

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
        
    new_iter, new_interval, new_ease, status, next_date = calculate_sm2(
        grade=review.grade,
        iterations=iterations,
        interval=interval,
        ease_factor=ease_factor,
        next_review_date=next_review_date
    )
    
    new_data = {
        "iterations": new_iter,
        "interval": new_interval,
        "ease_factor": new_ease,
        "status": status,
        "next_review_date": next_date,
        "last_reviewed_at": datetime.now(timezone.utc)
    }
    
    return crud_progress.create_or_update_progress(db, current_user.id, card_id, new_data)

@router.get("/progress/{card_id}", response_model=progress_schema.ProgressResponse)
def get_card_progress(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    progress = crud_progress.get_progress(db, current_user.id, card_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Henüz bu kartı çalışmadınız.")
    return progress
