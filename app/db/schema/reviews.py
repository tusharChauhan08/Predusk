from pydantic import BaseModel
from typing import Optional

class PostReviews(BaseModel):
    book_id: int
    ratings: int
    review: str
    reviewer_name: str

class UpdateReviews(BaseModel):
    review_id: int
    ratings: Optional[int] = None
    review: Optional[str] = None