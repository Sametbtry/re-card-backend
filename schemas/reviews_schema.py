from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProgressBase(BaseModel):
    iterations: int
    interval: int
    ease_factor: float
    status: str
    next_review_date: datetime
    last_reviewed_at: Optional[datetime] = None

class ProgressResponse(ProgressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    card_id: int


class ReviewRequest(BaseModel):
    grade: int  # 0: Again, 1: Hard, 2: Good, 3: Easy
    card_id: int
