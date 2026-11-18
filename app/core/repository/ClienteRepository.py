from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ClienteModel import ClienteModel
from app.core.repository.BaseRepository import BaseRepository


class ClienteRepository(BaseRepository[ClienteModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ClienteModel)
