from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SPost(BaseModel):
    content: str


class SPostResponse(SPost):

    id: int
    user_id: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True