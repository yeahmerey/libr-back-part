from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from app.db.db_config import Base


class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    following_id = Column(Integer, ForeignKey('users.id'))

    __table_args__ = (UniqueConstraint('follower_id', 'following_id', name='unique_follow'),)