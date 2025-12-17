from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.db_config import Base


class LikePost(Base):
    __tablename__ = 'likedposts'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_likepost'),)
