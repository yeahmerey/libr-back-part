# app/api/routes/admin.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException , Body
from sqlalchemy import select
from app.api.dependenies import get_current_admin  # ← твой исправленный путь
from app.db.models.content import Content
from app.db.models.user import User
from app.db.db_config import async_session_maker
from app.schemas.user import SUserPublic  # уже есть
from app.schemas.user_auth import SUserRegister
from app.services.auth import get_password_hash
from app.schemas.content import ContentCreate , ContentUpdate , ContentResponse
from pydantic import BaseModel
from typing import Literal , Optional

router = APIRouter(prefix="/admin", tags=["Admin"])

class SContentCreate(BaseModel):
    type: Literal["book", "movie"]
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class SContentUpdate(SContentCreate):
    pass

class SContentResponse(SContentCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/users", response_model=list[SUserPublic])
async def get_all_users(admin: User = Depends(get_current_admin)):
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users

@router.put("/users/{user_id}/toggle-admin")
async def toggle_user_admin(user_id: int, admin: User = Depends(get_current_admin)):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot change your own admin status")
    
    async with async_session_maker() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_admin = not user.is_admin
        await session.commit()
        return {"user_id": user_id, "is_admin": user.is_admin}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, admin: User = Depends(get_current_admin)):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    async with async_session_maker() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
        return {"message": "User deleted"}
    
@router.post("/users", status_code=201)
async def create_user(
    user_data: SUserRegister, 
    admin: User = Depends(get_current_admin)
):
    async with async_session_maker() as session:
        # Проверка уникальности
        existing = await session.execute(
            select(User).where((User.email == user_data.email) | (User.username == user_data.username))
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            is_admin=False  # по умолчанию не админ
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }

@router.put("/users/{user_id}/username")
async def update_username(
    user_id: int,
    new_username: str = Body(..., embed=True),
    admin: User = Depends(get_current_admin)
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot change your own username via admin panel")
    
    async with async_session_maker() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Проверка уникальности
        existing = await session.execute(
            select(User).where(User.username == new_username, User.id != user_id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken")
        
        user.username = new_username
        await session.commit()
        return {"id": user_id, "username": new_username}

@router.post("/content", response_model=ContentResponse)
async def create_content(data: SContentCreate, admin: User = Depends(get_current_admin)):
    async with async_session_maker() as session:
        new = Content(**data.model_dump())
        session.add(new)
        await session.commit()
        await session.refresh(new)
        return new

@router.put("/content/{content_id}", response_model=SContentResponse)
async def update_content(
    content_id: int,
    data: SContentUpdate,
    admin: User = Depends(get_current_admin)
):
    async with async_session_maker() as session:
        item = await session.get(Content, content_id)
        if not item:
            raise HTTPException(404, "Content not found")
        for k, v in data.model_dump().items():
            setattr(item, k, v)
        await session.commit()
        await session.refresh(item)
        return item

@router.delete("/content/{content_id}")
async def delete_content(content_id: int, admin: User = Depends(get_current_admin)):
    async with async_session_maker() as session:
        item = await session.get(Content, content_id)
        if not item:
            raise HTTPException(404, "Content not found")
        await session.delete(item)
        await session.commit()
        return {"message": "Deleted"}