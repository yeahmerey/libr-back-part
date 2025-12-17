from sqlalchemy import delete, select, func

from app.db.db_config import async_session_maker
from app.db.models.likecomment import LikeComment
from app.db.repositories.base import BaseDAO


class LikeCommentDAO(BaseDAO):
    model = LikeComment

    @classmethod
    async def delete_like(cls, comment_id: int, user_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.comment_id == comment_id, cls.model.user_id == user_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_post_likes_count(cls, comment_id: int):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id)).where(cls.model.comment_id == comment_id)
            result = await session.execute(query)
            return result.scalars().all()
