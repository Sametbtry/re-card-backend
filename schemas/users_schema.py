from pydantic import BaseModel
from datetime import datetime

# /users/me endpoint response
class UserProfileResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    total_cards_count: int
    studied_cards_count: int
    learned_cards_count: int
    
