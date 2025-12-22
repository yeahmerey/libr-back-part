from fastapi import APIRouter, Depends, HTTPException
from app.api.dependenies import get_current_user
from app.db.models.user import User
from app.services.follow import FollowService

router = APIRouter(prefix="/users", tags=["Follow"])

@router.post("/{user_id}/follow")
async def toggle_follow(user_id: int, current_user: User = Depends(get_current_user)):
    await FollowService.toggle_follow(follower_id=current_user.id, following_id=user_id)
    return {"message": "Follow status updated"}

@router.get("/{user_id}/followers")
async def get_followers(user_id: int):
    return await FollowService.get_followers(user_id)

@router.get("/{user_id}/following")
async def get_following(user_id: int):
    return await FollowService.get_following(user_id)