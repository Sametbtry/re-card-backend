from pydantic import BaseModel, ConfigDict

# /users/me/stats endpoint response
class UserProfileStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    total_cards_count: int
    studied_cards_count: int
    learned_cards_count: int
    
