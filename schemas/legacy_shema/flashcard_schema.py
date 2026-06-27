from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FlashcardBase(BaseModel):
    word: str
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    translation: str
    is_public: Optional[bool] = False
    image_url: Optional[str] = None

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    word: Optional[str] = None
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    translation: Optional[str] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None

class FlashcardResponse(FlashcardBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlashcardPaginatedResponse(BaseModel):
    items: list[FlashcardResponse]
    total: int
    page: int
    size: int
    total_pages: int
