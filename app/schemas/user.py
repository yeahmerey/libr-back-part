from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SUser(BaseModel):
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    year_of_birth: Optional[int] = None

class SUserPublic(SUser):
    id: int
    created_at: datetime

    class Config:
        from_attributes=True
