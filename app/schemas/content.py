# app/schemas/content.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing_extensions import Literal  # для поддержки Literal в старых версиях

# Используй это, если Python >= 3.8 и Pydantic >= 2.0
ContentType = Literal["book", "movie"]


class ContentBase(BaseModel):
    type: ContentType
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class ContentCreate(ContentBase):
    pass


class ContentUpdate(ContentBase):
    pass


class ContentResponse(ContentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # ← включает поддержку SQLAlchemy моделей