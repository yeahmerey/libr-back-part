from datetime import datetime

from pydantic import BaseModel


class SPost(BaseModel):
    content: str


class SPostResponse(SPost):

    id: int
    user_id: int
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True