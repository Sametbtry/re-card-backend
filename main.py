from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, flashcards, review

# Tabloları oluştur (Alembic yoksa otomatik oluşturmak için)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flashcard PWA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(review.router, prefix="/api/cards/review", tags=["review"])
app.include_router(flashcards.router, prefix="/api/cards", tags=["cards"])

@app.get("/")
def read_root():
    return {"message": "Flashcard PWA Backend is running"}
