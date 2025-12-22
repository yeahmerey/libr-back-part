# app/api/routes/ai.py
from fastapi import APIRouter, HTTPException, Body, Depends
from app.api.dependenies import get_current_user  # ← твой существующий зависимость
from app.db.repositories.chat_message import ChatMessageDAO
import httpx
from app.core.settings import settings
from sqlalchemy import delete
from app.db.models.chat_message import ChatMessage
from app.db.db_config import async_session_maker
router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat")
async def chat_with_gemini(
    message: str = Body(..., embed=True),
    current_user = Depends(get_current_user)  # ← аутентифицируем пользователя
):
    user_id = current_user.id

    # Сохраняем сообщение пользователя
    await ChatMessageDAO.create(user_id=user_id, sender="user", content=message)

    # Получаем последние 10 сообщений для контекста (опционально)
    history_db = await ChatMessageDAO.get_last_messages(user_id, limit=10)
    history = [
        {"role": "user" if msg.sender == "user" else "model", "parts": [{"text": msg.content}]}
        for msg in history_db
        if msg.sender in ("user", "ai")  # пропускаем, если есть другие типы
    ]

    # Вызов Gemini
    API_KEY = settings.GEMINI_API_KEY
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    params = {"key": API_KEY}
    guided_message = (
    "You are an expert in books and movies. "
    "Only answer questions about literature and films. "
    "If the topic is unrelated, politely say you only discuss books and movies. "
    "Now respond to this: " + message
    )

    contents = history + [{"role": "user", "parts": [{"text": guided_message}]}]
    payload = {"contents": contents}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, params=params, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            reply_text = data["candidates"][0]["content"]["parts"][0].get("text", "").strip()
            if not reply_text:
                reply_text = "I couldn't generate a response."

            # Сохраняем ответ AI
            await ChatMessageDAO.create(user_id=user_id, sender="ai", content=reply_text)

            return {"reply": reply_text}

        except Exception as e:
            error_msg = f"AI error: {str(e)}"
            await ChatMessageDAO.create(user_id=user_id, sender="ai", content=error_msg)
            raise HTTPException(status_code=500, detail="AI service failed")
        

@router.get("/history")
async def get_chat_history(current_user = Depends(get_current_user)):
    messages = await ChatMessageDAO.get_last_messages(current_user.id, limit=10)
    return [
        {"sender": msg.sender, "text": msg.content}
        for msg in messages
    ]


@router.delete("/history")
async def clear_chat_history(current_user = Depends(get_current_user)):
    async with async_session_maker() as session:
        await session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == current_user.id)
        )
        await session.commit()
    return {"message": "Chat history cleared"}