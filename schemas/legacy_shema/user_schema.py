import re
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

def validate_password_strength(v: str) -> str:
    if len(v) < 8 or not re.search(r"\d", v) or not re.search(r"[a-zA-Z]", v):
        raise ValueError('Şifre en az 8 karakter, 1 harf ve 1 sayı içermelidir')
    return v

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def password_valid(cls, v: str) -> str:
        return validate_password_strength(v)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def password_valid(cls, v: str) -> str:
        return validate_password_strength(v)

class EmailChangeRequest(BaseModel):
    new_email: str

class MessageResponse(BaseModel):
    message: str

class UserProfileResponse(UserBase):
    id: int
    created_at: datetime
    total_cards_count: int
    studied_cards_count: int
    learned_cards_count: int
    
