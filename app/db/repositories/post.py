from sqlalchemy import select , insert , update

from app.db.db_config import async_session_maker
from app.db.models.comment import Comment
from app.db.models.post import Post
from app.db.repositories.base import BaseDAO
from app.schemas.post import SPostResponse


class PostDAO(BaseDAO):
    model = Post
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            # Вставляем и получаем возвращённую строку
            stmt = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            new_obj = result.scalar()
            return new_obj

    @classmethod
    async def get_post_comments(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(Comment).where(Comment.post_id == post_id)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def search_post(cls, text: str) -> list[SPostResponse]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.content.ilike(f"%{text}%"))
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts
    @classmethod
    async def update(cls, id: int, **data):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == id).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()