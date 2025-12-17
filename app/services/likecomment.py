from app.db.repositories.likecomment import LikeCommentDAO


class LikeCommentService:

    @classmethod
    async def get_post_likes_count(cls, comment_id: int):
        return await LikeCommentDAO.get_post_likes_count(comment_id=comment_id)

    @classmethod
    async def toggle_like(cls, comment_id: int, user_id: int):
        like = await LikeCommentDAO.find_one_or_none(comment_id=comment_id, user_id=user_id)
        if like:
            await LikeCommentDAO.delete_like(comment_id=comment_id, user_id=user_id)
            return {"message": "Like removed"}
        await LikeCommentDAO.add(comment_id=comment_id, user_id=user_id)
        return {"message": "Like added"}