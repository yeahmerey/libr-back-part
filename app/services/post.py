import os
import uuid
import aiofiles

from fastapi import HTTPException, UploadFile

from app.db.repositories.comment import CommentDAO
from app.db.repositories.post import PostDAO
from app.schemas.comment import SCommentResponse, SComment
from app.schemas.post import SPost, SPostResponse


class PostServices:


    @classmethod
    async def get_all_posts(cls) -> list[SPostResponse]:
        posts = await PostDAO.find_all()
        return posts

    @classmethod
    async def get_post(cls, post_id: int) -> SPostResponse:
        post = await PostDAO.find_one_or_none(id=post_id)
        return post

    @classmethod
    async def add_post(cls, post: SPost, file: UploadFile, user_id: int) :
        image_url = None

        if file:
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Content type not supported")

            extension = file.filename.split(".")[-1]
            unique_name = f"{uuid.uuid4()}.{extension}"
            file_path = os.path.join("app/static/images", unique_name)

            async with aiofiles.open(file_path, "wb") as new_file:
                content = await file.read()
                await new_file.write(content)

            image_url = file_path

        return await PostDAO.add(content=post.content, image_url=image_url, user_id=user_id)

    @classmethod
    async def edit_post(cls, post: SPost, post_id: int, user_id: int):
        existing_post = await PostDAO.find_one_or_none(id=post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")

        if existing_post.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return PostDAO.update(content=post.content, image_url=post.image_url, id=post_id)

    @classmethod
    async def delete_post(cls, post_id: int, user_id: int):
        post = await PostDAO.find_one_or_none(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="You can delete only your own posts")

        return await PostDAO.delete(id=post_id)

    @classmethod
    async def get_post_comments(cls, post_id: int) -> list[SCommentResponse]:
        post_comments = await PostDAO.get_post_comments(post_id=post_id)
        if not post_comments:
            raise HTTPException(status_code=404, detail="Post not found")
        return post_comments

    @classmethod
    async def add_comment(cls, comment: SComment, post_id: int, user_id: int):
        return await CommentDAO.add(content=comment.content, post_id=post_id, user_id=user_id)

    @classmethod
    async def search_posts(cls, query: str) -> list[SPostResponse]:
        return await PostDAO.search_post(query)
