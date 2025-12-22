from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import relationship

from app.db.db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    image_url = Column(String(255), unique=True)
    bio = Column(String(255))
    location = Column(String(100))
    year_of_birth = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    is_admin = Column(Boolean , default=False , nullable=False)
