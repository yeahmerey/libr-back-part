from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select
from app.db.models.content import Content
from app.db.db_config import async_session_maker

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