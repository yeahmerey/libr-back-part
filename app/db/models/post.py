from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.db_config import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))