from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# /api/v2/cards/ (Create a new flashcard)
class CardBase(BaseModel):
    word: str
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    translation: str
    is_public: Optional[bool] = False
    image_url: Optional[str] = None

class CardUpdate(BaseModel):
    word: Optional[str] = None
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    translation: Optional[str] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None

class CardResponse(CardBase):
    model_config = ConfigDict(from_attributes=True) 

    id: int
    creator_id: int
    created_at: datetime

class CardPaginatedResponse(BaseModel):
    items: list[CardResponse]
    total: int
    page: int
    size: int
    total_pages: int    

class ImageSearchResponse(BaseModel):
    image_url: Optional[str] = None
    