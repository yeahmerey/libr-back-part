from fastapi import APIRouter, Depends

from app.api.dependenies import get_current_user
from app.db.models.user import User
from app.services.likecomment import LikeCommentService

router = APIRouter(
    prefix="/comment/{comment_id}/like",
    tags=["Like-comment"]
)

@router.post("")
async def toggle_like(comment_id: int, user: User = Depends(get_current_user)):
    return await LikeCommentService.toggle_like(comment_id=comment_id, user_id=user.id)

@router.get("")
async def get_post_likes_count(comment_id: int):
    return await LikeCommentService.get_post_likes_count(comment_id=comment_id)
