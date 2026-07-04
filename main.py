from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, auth, flashcards, review

# Tabloları oluştur (Alembic yoksa otomatik oluşturmak için)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Re-Card API", version="2.0.0", description="Re-Card is a flashcard application that helps you learn new words faster.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.re-card.app",
        "https://re-card.app",
        "https://re-card-frontend.vercel.app",
        "http://localhost:5173", 
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v2/auth", tags=["Authentication"]) 
app.include_router(review.router, prefix="/api/v2/reviews", tags=["Reviews"])
app.include_router(flashcards.router, prefix="/api/v2/cards", tags=["Cards"])
app.include_router(users.router, prefix="/api/v2/users", tags=["Users"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Re-Card Backend is running"}
