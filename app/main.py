from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.post import router as post_router
from app.api.routes.likepost import router as likepost_router
from app.api.routes.likecomment import router as likecomment_router
from app.api.routes.image import router as image_router

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decoratot import cache
#
# from redis import asyncio as aioredis


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(likepost_router)
app.include_router(likecomment_router)
app.include_router(image_router)