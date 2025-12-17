from fastapi import APIRouter, Depends, HTTPException

from app.db.repositories.comment import CommentDAO

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

