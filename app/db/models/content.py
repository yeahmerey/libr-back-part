# app/db/models/content.py
from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, func
from app.db.db_config import Base

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum("book", "movie", name="content_type"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ← так правильно