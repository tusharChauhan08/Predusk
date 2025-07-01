from pydantic import BaseModel
from typing import Optional

class CreateBooks(BaseModel):
    book_name: str
    author: str
    description: str
    language: str

class UpdateBooks(BaseModel):
    book_name: Optional[str] = None 
    author: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None