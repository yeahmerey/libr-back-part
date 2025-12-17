import os
import uuid
import aiofiles

from fastapi import UploadFile, HTTPException

from app.db.repositories.user import UserDAO
from app.schemas.user import SUserPublic, SUser


class UserService:

    @classmethod
    async def get_all(cls) -> list[SUserPublic]:
        return await UserDAO.find_all()

    @classmethod
    async def update(cls, user_id: int, updated_user: SUser):
        return await UserDAO.update(id=user_id, username=updated_user.username, bio=updated_user.bio)

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
    async def add_user_image(cls, file: UploadFile, user_id: int):
        if not file.content_type.startswith('image'):
            raise HTTPException(status_code=404, detail="Image not supported")

        extension = file.filename.split('.')[-1]
        unique_name = f"{uuid.uuid4().hex}.{extension}"
        file_path = os.path.join("app/static/images", unique_name)

        async with aiofiles.open(file_path, 'wb') as file_object:
            content = await file.read()
            await file_object.write(content)

        return await UserDAO.add_user_image(file_path, user_id=user_id)