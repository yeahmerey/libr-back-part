from typing import Union

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy import select
from app.db.db_config import async_session_maker
from app.db.models.post import Post
from app.schemas.comment import SComment, SCommentResponse
from app.services.post import PostServices
from app.api.routes.user import get_current_user
from app.db.models.user import User
from app.schemas.post import SPost, SPostResponse

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("")
async def get_posts():
    async with async_session_maker() as session:
        result = await session.execute(
            select(Post).order_by(Post.created_at.desc())  # ← должно быть
        )
        return result.scalars().all()
    
@router.post("", response_model=SPostResponse)
async def create_post(content: str = Form(...), file: Union[UploadFile, str] = File(None), user: User = Depends(get_current_user)):
    from app.schemas.post import SPost
    post = SPost(content=content)
    return await PostServices.add_post(post, file, user.id)

@router.get("/search", response_model=list[SPostResponse])
async def search_posts(query: str = Query(..., min_length=1, max_length=50)):
    return await PostServices.search_posts(query)

@router.get("/{id}", response_model=SPostResponse)
async def get_post_by_id(id: int):
    return PostServices.get_post(post_id=id)

# app/api/routes/post.py

@router.put("/{id}", response_model=SPostResponse)
async def update_post(
    id: int,
    content: str = Form(...),
    file: UploadFile = File(None),
    user: User = Depends(get_current_user)
):
    from app.schemas.post import SPost
    post = SPost(content=content)
    return await PostServices.edit_post(post=post, post_id=id, user_id=user.id, file=file)
@router.delete("/{id}")
async def delete_post(id: int, user: User = Depends(get_current_user)):
    return await PostServices.delete_post(post_id=id, user_id=user.id)

@router.get("/{id}/comments", response_model=list[SCommentResponse])
async def get_post_comments(post_id: int, user: User = Depends(get_current_user)):
    return await PostServices.get_post_comments(post_id=post_id)

@router.post("/{id}/comments")
async def create_post_comment(comment: SComment, post_id: int, user: User = Depends(get_current_user)):
    return await PostServices.add_comment(comment=comment, post_id=post_id, user_id=user.id)