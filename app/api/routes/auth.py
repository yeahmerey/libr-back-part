from fastapi import HTTPException

from fastapi import APIRouter, Response, Cookie
from jose import jwt, JWTError

from app.core.settings import settings
from app.db.repositories.user import UserDAO
from app.schemas.user_auth import SUserAuth, SUserRegister
from app.services.auth import get_password_hash, verify_password, create_access_token, authenticate_user, \
    create_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def register(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hash_password = get_password_hash(user_data.password)
    await UserDAO.add(username=user_data.username, email=user_data.email, password=hash_password)

@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"message": "Successfully logged in"}

@router.post("/refresh")
async def refresh(response: Response, refresh_token: str = Cookie(None, alias="refresh_token")):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token({"sub": str(user_id)})
    refresh_token = create_refresh_token({"sub": str(user_id)})

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {"message": "Successfully refreshed"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")