from datetime import datetime

from pydantic import BaseModel


class SComment(BaseModel):

    content: str

class SCommentResponse(SComment):

    id: int
    content: str
    created_at: datetime
    post_id: int
    user_id: int