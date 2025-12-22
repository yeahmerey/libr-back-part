# app/api/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException , Body
from sqlalchemy import select
from app.api.dependenies import get_current_admin  # ← твой исправленный путь
from app.db.models.user import User
from app.db.db_config import async_session_maker
from app.schemas.user import SUserPublic  # уже есть
from app.schemas.user_auth import SUserRegister
from app.services.auth import get_password_hash
router = APIRouter(prefix="/admin", tags=["Admin"])

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