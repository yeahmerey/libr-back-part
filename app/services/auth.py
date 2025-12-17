from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core.settings import settings
from app.db.repositories.user import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password:str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.REFRESH_KEY, algorithm=settings.ALGORITHM)



def verify_token(token: str, key: str):
    try:
        payload = jwt.decode(token, key, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None