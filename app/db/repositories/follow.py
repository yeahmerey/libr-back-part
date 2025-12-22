from sqlalchemy import select
from app.db.db_config import async_session_maker
from app.db.models.follow import Follow
from app.db.models.user import User

class FollowDAO:

    @classmethod
    async def add_follow(cls, follower_id: int, following_id: int):
        async with async_session_maker() as session:
            from sqlalchemy import insert
            stmt = insert(Follow).values(follower_id=follower_id, following_id=following_id)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_follow(cls, follower_id: int, following_id: int):
        async with async_session_maker() as session:
            from sqlalchemy import delete
            stmt = delete(Follow).where(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_follow(cls, follower_id: int, following_id: int):
        async with async_session_maker() as session:
            query = select(Follow).where(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_followers(cls, user_id: int):
        """Получить пользователей, которые подписаны на user_id"""
        async with async_session_maker() as session:
            query = (
                select(User)
                .join(Follow, Follow.follower_id == User.id)
                .where(Follow.following_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_following(cls, user_id: int):
        """Получить пользователей, на которых подписан user_id"""
        async with async_session_maker() as session:
            query = (
                select(User)
                .join(Follow, Follow.following_id == User.id)
                .where(Follow.follower_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()