from typing import List
from app.db.db_config import async_session_maker
from app.db.models.chat_message import ChatMessage
from sqlalchemy import select
class ChatMessageDAO:
    model = ChatMessage

    
    
    @classmethod
    async def get_last_messages(cls, user_id: int, limit: int = 10) -> List[ChatMessage]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model)  # ← ORM-запрос, возвращает объекты модели
                .where(cls.model.user_id == user_id)
                .order_by(cls.model.created_at.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
            return list(reversed(messages))
    @classmethod
    async def create(cls, user_id: int, sender: str, content: str) -> ChatMessage:
        async with async_session_maker() as session:
            new_message = cls.model(user_id=user_id, sender=sender, content=content)
            session.add(new_message)
            await session.commit()
            await session.refresh(new_message)
            return new_message