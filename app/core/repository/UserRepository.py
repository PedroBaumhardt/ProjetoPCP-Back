from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.UserModel import UserModel
from app.core.repository.BaseRepository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)
