from fastapi import APIRouter, UploadFile, Depends

from app.api.routes.user import get_current_user
from app.db.models.user import User
from app.services.user import UserService

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


@router.post("")
async def add_user_image(file: UploadFile, user: User = Depends(get_current_user)):
    return await UserService.add_user_image(file=file, user_id=user.id)