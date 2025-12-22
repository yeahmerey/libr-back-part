from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select , func
from app.db.models.content import Content
from app.db.models.review import Review
from app.db.models.user import User
from app.api.dependenies import get_current_user
from app.db.db_config import async_session_maker
from app.schemas.review import ReviewCreate
router = APIRouter(prefix="/content", tags=["Content"])

@router.get("")
async def list_content(
    q: str = Query(None, min_length=1),
    type: str = Query(None, regex="^(book|movie)$")
):
    async with async_session_maker() as session:
        query = select(Content)
        if q:
            query = query.where(Content.name.ilike(f"%{q}%"))
        if type:
            query = query.where(Content.type == type)
        result = await session.execute(query)
        return result.scalars().all()

@router.get("/{content_id}")
async def get_content_detail(content_id: int):
    async with async_session_maker() as session:
        item = await session.get(Content, content_id)
        if not item:
            raise HTTPException(404, "Content not found")
        return item

@router.post("/{content_id}/reviews")
async def create_review(
    content_id: int,
    review_data: ReviewCreate,               # ← теперь JSON из тела
    user = Depends(get_current_user)
):
    async with async_session_maker() as session:
        content = await session.get(Content, content_id)
        if not content:
            raise HTTPException(404, "Content not found")
        
        review = Review(
            user_id=user.id,
            content_id=content_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        session.add(review)
        await session.commit()
        return {"message": "Review added"}
    
@router.get("/{content_id}/reviews")
async def get_reviews(content_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Review, User.username)
            .join(User, Review.user_id == User.id)
            .where(Review.content_id == content_id)
            .order_by(Review.created_at.desc())
        )
        return [
            {
                "username": username,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat()
            }
            for review, username in result
        ]

@router.get("/{content_id}/average-rating")
async def get_average_rating(content_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.avg(Review.rating)).where(Review.content_id == content_id)
        )
        avg = result.scalar()
        return {"average_rating": round(avg, 1) if avg else None}
    