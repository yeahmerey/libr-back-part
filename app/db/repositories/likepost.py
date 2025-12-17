from sqlalchemy import delete, select, func

from app.db.db_config import async_session_maker
from app.db.models.likepost import LikePost
from app.db.repositories.base import BaseDAO


class LikePostDAO(BaseDAO):
    model = LikePost

    @classmethod
    async def delete_like(cls, post_id: int, user_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.post_id == post_id, cls.model.user_id == user_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_post_likes_count(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id)).where(cls.model.post_id == post_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_liked_posts(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where()