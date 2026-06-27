from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CardBase(BaseModel):
    word: str
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    translation: str
    is_public: Optional[bool] = False
    image_url: Optional[str] = None

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    word: Optional[str] = None
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    translation: Optional[str] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None

class CardResponse(CardBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CardPaginatedResponse(BaseModel):
    items: list[CardResponse]
    total: int
    page: int
    size: int
    total_pages: int

class ImageSearchResponse(BaseModel):
    image_url: str | None = None
    