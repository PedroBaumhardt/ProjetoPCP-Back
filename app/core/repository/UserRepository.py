from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.model.UserModel import UserModel
from app.core.repository.BaseRepository import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_email(self, email: str) -> UserModel | None:
        qry = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(qry)
        return result.scalars().one_or_none()