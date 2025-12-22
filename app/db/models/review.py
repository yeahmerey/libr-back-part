# app/db/models/review.py
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from app.db.db_config import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1–5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())