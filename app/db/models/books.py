from sqlalchemy import Integer, Column, String, Text
from sqlalchemy.orm import relationship
from app.core.config import settings
from app.db.base_mixin import TimestampMixin

class Books(TimestampMixin):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    language = Column(String, nullable=False)

    reviews = relationship("Reviews", back_populates="book", cascade=settings.CASCADE)