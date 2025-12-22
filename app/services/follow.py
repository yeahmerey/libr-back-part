from app.db.repositories.follow import FollowDAO

class FollowService:

    @classmethod
    async def toggle_follow(cls, follower_id: int, following_id: int):
        """Переключить подписку"""
        follow = await FollowDAO.get_follow(follower_id, following_id)
        if follow:
            await FollowDAO.delete_follow(follower_id, following_id)
        else:
            await FollowDAO.add_follow(follower_id, following_id)

    @classmethod
    async def get_followers(cls, user_id: int):
        """Получить подписчиков пользователя"""
        return await FollowDAO.get_followers(user_id)

    @classmethod
    async def get_following(cls, user_id: int):
        """Получить подписки пользователя"""
        return await FollowDAO.get_following(user_id)