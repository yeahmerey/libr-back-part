from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.db_config import Base


class LikeComment(Base):
    __tablename__ = 'likedcomments'

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    __table_args__ = (UniqueConstraint('user_id', 'comment_id', name='unique_likecomment'),)
