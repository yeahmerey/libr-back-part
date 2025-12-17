from fastapi import APIRouter, Depends

from app.api.dependenies import get_current_user
from app.db.models.user import User
from app.db.repositories.likepost import LikePostDAO
from app.services.likepost import LikePostService

router = APIRouter(
    prefix="/post/{post_id}/like",
    tags=["Like"]
)

@router.post("")
async def toggle_like(post_id: int, user: User = Depends(get_current_user)):
    return await LikePostService.toggle_like(post_id=post_id, user_id=user.id)

@router.get("")
async def get_post_likes_count(post_id: int):
    return await LikePostService.get_post_likes_count(post_id=post_id)