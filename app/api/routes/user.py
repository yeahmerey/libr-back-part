from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from app.db.db_config import async_session_maker

from app.api.dependenies import get_current_user
from app.db.models.content import Content
from app.db.models.review import Review
from app.db.models.user import User
from app.schemas.post import SPostResponse
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

@router.get("/posts", response_model=list[SPostResponse])
async def get_user_posts(user: User = Depends(get_current_user)):
    return await UserService.get_user_posts(user.id)

@router.get("/{id}", response_model=SUserPublic)
async def get_user_by_id(id: int):
    user = await UserDAO.find_one_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{id}/posts", response_model=list[SPostResponse])
async def get_user_public_posts(id: int):
    return await UserService.get_user_posts(user_id=id)


@router.get("/{id}/liked-posts")
async def get_liked_posts(user: User = Depends(get_current_user)):
    return await UserService.get_user_liked_posts(user_id=user.id)

@router.put("/me")
async def update_user(updated_user: SUser ,user: User = Depends(get_current_user)):
    await UserService.update(user_id=user.id , updated_user=updated_user)
    return await UserDAO.find_one_or_none(id=user.id)

@router.get("/{user_id}/reviews")
async def get_user_reviews(user_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Review, Content.name, Content.type)
            .join(Content, Review.content_id == Content.id)
            .where(Review.user_id == user_id)
            .order_by(Review.created_at.desc())
        )
        return [
            {
                "content_id": review.content_id,
                "content_name": name,
                "content_type": type,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat()
            }
            for review, name, type in result
        ]