from fastapi import APIRouter, Depends, Query

from app.api.dependenies import get_current_user
from app.db.models.user import User
from app.schemas.user import SUserPublic, SUser
from app.services.user import UserService
from app.db.repositories.user import UserDAO
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("", response_model=list[SUserPublic])
async def get_all_users():
    return await UserService.get_all()

@router.get("/me", response_model=SUserPublic)
async def get_current_user(user: User = Depends(get_current_user)):
    return user

@router.get("/search", response_model=list[SUserPublic])
async def user_search(query: str = Query(..., min_length=1, max_length=50)):
    return await UserService.get_users(query)

@router.get("/posts")
async def get_user_posts(user: User = Depends(get_current_user)):
    return await UserService.get_user_posts(user.id)

@router.put("/me")
async def update_user(updated_user: SUser ,user: User = Depends(get_current_user)):
    await UserService.update(user_id=user.id , updated_user=updated_user)
    return await UserDAO.find_one_or_none(id=user.id)

@router.get("/{id}/liked-posts")
async def get_liked_posts(user: User = Depends(get_current_user)):
    return await UserService.get_user_liked_posts(user_id=user.id)