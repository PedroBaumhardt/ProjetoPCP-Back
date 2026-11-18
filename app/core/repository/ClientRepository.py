from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ClientModel import ClientModel
from app.core.repository.BaseRepository import BaseRepository


class ClientRepository(BaseRepository[ClientModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ClientModel)
