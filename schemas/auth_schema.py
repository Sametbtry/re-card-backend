import re
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

def validate_password_strength(v: str) -> str:
    if len(v) < 8 or not re.search(r"\d", v) or not re.search(r"[a-zA-Z]", v):
        raise ValueError('Şifre en az 8 karakter, 1 harf ve 1 sayı içermelidir')
    return v

# register request
class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def password_valid(cls, v: str) -> str:
        return validate_password_strength(v)

# register response
class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True 

# login response
class Token(BaseModel):
    access_token: str
    token_type: str

# token data from the JWT
class TokenData(BaseModel):
    username: Optional[str] = None