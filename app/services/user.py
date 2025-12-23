import os
import uuid
import aiofiles

from fastapi import UploadFile, HTTPException
from sqlalchemy import select

from app.db.models.follow import Follow
from app.db.models.user import User
from app.db.repositories.user import UserDAO
from app.schemas.user import SUserPublic, SUser
from app.db.db_config import async_session_maker

class UserService:

    @classmethod
    async def get_all(cls) -> list[SUserPublic]:
        return await UserDAO.find_all()

    @classmethod
    async def update(cls, user_id: int, updated_user: SUser):
        update_data = updated_user.model_dump(exclude_unset=True)
        protected_fields = {"id", "email"}
        update_data = {k : v for k, v in update_data.items() if k not in protected_fields}

        return await UserDAO.update(id=user_id,**update_data)

    @classmethod
    async def get_users(cls, query: str) -> list[SUserPublic]:
        return await UserDAO.search_user(query)

    @classmethod
    async def get_user_liked_posts(cls, user_id: int):
        return await UserDAO.get_user_liked_posts(user_id=user_id)

    @classmethod
    async def get_user_posts(cls, user_id: int):
        return await UserDAO.get_user_posts(user_id=user_id)

    @classmethod
    @classmethod  # ← ОБЯЗАТЕЛЬНО @classmethod
    async def add_user_image(cls, file: UploadFile, user_id: int):
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")

        extension = file.filename.split(".")[-1]
        unique_name = f"{uuid.uuid4().hex}.{extension}"
        file_path = os.path.join("app", "static", "images", unique_name)

        # Создаём папку, если её нет
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        # 🔥 Сохраняем ОТНОСИТЕЛЬНЫЙ путь для фронтенда
        image_url = f"/static/images/{unique_name}"
        return await UserDAO.add_user_image(image_url=image_url, user_id=user_id)
    
    @classmethod
    async def search_users_with_follow_status(cls, query: str, current_user_id: int = None):
        async with async_session_maker() as session:
            # Основной запрос: пользователи
            users_query = select(User).where(User.username.ilike(f"%{query}%"))
            users_result = await session.execute(users_query)
            users = users_result.scalars().all()

            if not current_user_id:
                return [{"user": u, "is_following": False} for u in users]

            # Получаем ID тех, на кого подписан current_user
            following_subq = (
                select(Follow.following_id)
                .where(Follow.follower_id == current_user_id)
                .subquery()
            )
            following_ids_query = select(following_subq.c.following_id)
            following_ids = set(await session.scalars(following_ids_query).all())

            return [
                {
                    "user": u,
                    "is_following": u.id in following_ids
                }
                for u in users
            ]