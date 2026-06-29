import re
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

def space_control(v: str) -> str:
    if ' ' in v:
        raise ValueError("Kullanıcı adı ve şifre boşluk içeremez")
    return v 

def password_strength(v: str) -> str:
    if len(v) < 8 or not re.search(r"\d", v) or not re.search(r"[a-zA-Z]", v):
        raise ValueError('Şifre en az 8 karakter, 1 harf ve 1 sayı içermelidir')
    return v

# register request
class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username", "password")
    @classmethod
    def space_control_valid(cls, v: str) -> str:
        return space_control(v)

    @field_validator('password')
    @classmethod
    def password_strength_valid(cls, v: str) -> str:
        return password_strength(v)

# register response
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    id: int
    username: str
    created_at: datetime

# login response
class Token(BaseModel):
    access_token: str
    token_type: str