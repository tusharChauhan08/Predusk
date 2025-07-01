from sqlalchemy import Text, String, Integer, ForeignKey, Column
from sqlalchemy.orm import relationship
from app.core.config import settings
from app.db.base_mixin import TimestampMixin
from app.db.base import Base

class Reviews(Base, TimestampMixin):
    __tablename__ = "reviews"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    reviewer_name = Column(String, nullable=False)
    ratings = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)

    book = relationship("Books", back_populates="reviews")