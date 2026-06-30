from sqlalchemy.sql.functions import current_user
from fastapi import APIRouter, Depends

from schemas.users_schema import UserProfileStats
from .auth import get_current_user

router = APIRouter()

@router.get("/me/stats", response_model=UserProfileStats, summary="Get user stats")
def get_my_profile(current_user = Depends(get_current_user)):

    # The "or []" was implemented to prevent model relationships from becoming none
    total_cards_count = len(current_user.flashcards or []) 
    studied_cards_count = len(current_user.progress or [])
    learned_cards_count = sum(1 for p in current_user.progress or [] if p.status == "mastered")

    return UserProfileStats(
        username = current_user.username,
        total_cards_count = total_cards_count,
        studied_cards_count = studied_cards_count,
        learned_cards_count = learned_cards_count
    )
