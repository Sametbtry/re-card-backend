from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from database import get_db
from config import settings
from schemas import user_schema
from crud import crud_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten mevcut")
    
    if user.email:
        db_email = crud_user.get_user_by_email(db, email=user.email)
        if db_email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    return crud_user.create_user(db=db, user=user)

@router.post("/login", response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(db, form_data.username)
    if not user or not crud_user.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="kullanıcı adı veya şifre yanlış",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    total_cards_count = len(current_user.flashcards) if current_user.flashcards else 0
    studied_cards_count = 0
    learned_cards_count = 0
    
    if current_user.progress:
        studied_cards_count = len(current_user.progress)
        learned_cards_count = sum(1 for p in current_user.progress if p.status == "mastered")
        
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "total_cards_count": total_cards_count,
        "studied_cards_count": studied_cards_count,
        "learned_cards_count": learned_cards_count
    }

@router.post("/change-password")
def change_password(
    data: user_schema.PasswordChangeRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not crud_user.verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Mevcut şifre yanlış")
    
    current_user.password_hash = crud_user.get_password_hash(data.new_password)
    db.commit()
    return {"message": "Şifre başarıyla güncellendi"}

@router.post("/change-email")
def change_email(
    data: user_schema.EmailChangeRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.new_email:
        existing_user = crud_user.get_user_by_email(db, email=data.new_email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten kullanımda")
            
    current_user.email = data.new_email
    db.commit()
    return {"message": "E-posta başarıyla güncellendi"}

