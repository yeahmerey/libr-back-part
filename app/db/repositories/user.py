from fastapi import HTTPException
from sqlalchemy import select

from app.db.db_config import async_session_maker
from app.db.models.likepost import LikePost
from app.db.models.post import Post
from app.db.models.user import User
from app.db.repositories.base import BaseDAO
from app.schemas.user import SUserPublic


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def search_user(cls, text: str) -> list[SUserPublic]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.username.ilike(f"%{text}%"))
            result = await session.execute(query)
            users = result.scalars().all()
            return users

    @classmethod
    async def get_user_liked_posts(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Post).join(
                LikePost, LikePost.post_id == Post.id
                ).where(
                    LikePost.user_id == user_id
                    )
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @classmethod
    async def get_user_posts(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Post).where(Post.user_id == user_id)
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @classmethod
    async def add_user_image(cls, image_url: str, user_id: int):
        async with async_session_maker() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.image_url = image_url
            await session.commit()