from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import books, reviews

app = FastAPI(title="Books review api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books, prefix=f"{settings.API_V1_STR}/books", tags=["Book"])
app.include_router(reviews, prefix=f"{settings.API_V1_STR}/reviews", tags=["Reviews"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to book review api"}