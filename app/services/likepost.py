from app.db.repositories.likepost import LikePostDAO


class LikePostService:

    @classmethod
    async def get_post_likes_count(cls, post_id: int):
        return await LikePostDAO.get_post_likes_count(post_id=post_id)

    @classmethod
    async def toggle_like(cls, post_id: int, user_id: int):
        like = await LikePostDAO.find_one_or_none(post_id=post_id, user_id=user_id)
        if like:
            await LikePostDAO.delete_like(post_id=post_id, user_id=user_id)
            return {"message": "Like removed"}
        await LikePostDAO.add(post_id=post_id, user_id=user_id)
        return {"message": "Like added"}