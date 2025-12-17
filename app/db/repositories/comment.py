from app.db.models.comment import Comment
from app.db.repositories.base import BaseDAO


class CommentDAO(BaseDAO):
    model = Comment