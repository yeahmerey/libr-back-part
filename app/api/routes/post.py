from typing import Union

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form

from app.schemas.comment import SComment, SCommentResponse
from app.services.post import PostServices
from app.api.routes.user import get_current_user
from app.db.models.user import User
from app.schemas.post import SPost, SPostResponse

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("", response_model=list[SPostResponse])
async def get_posts():
    return await PostServices.get_all_posts()

@router.post("")
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

@router.put("/{id}")
async def update_post(updated_post: SPost, id: int, user: User = Depends(get_current_user)):
    return await PostServices.edit_post(post=updated_post, post_id=id, user_id=user.id)

@router.delete("/{id}")
async def delete_post(id: int, user: User = Depends(get_current_user)):
    return await PostServices.delete_post(post_id=id, user_id=user.id)

@router.get("/{id}/comments", response_model=list[SCommentResponse])
async def get_post_comments(post_id: int, user: User = Depends(get_current_user)):
    return await PostServices.get_post_comments(post_id=post_id)

@router.post("/{id}/comments")
async def create_post_comment(comment: SComment, post_id: int, user: User = Depends(get_current_user)):
    return await PostServices.add_comment(comment=comment, post_id=post_id, user_id=user.id)