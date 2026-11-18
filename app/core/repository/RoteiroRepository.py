from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.RoteiroModel import RoteiroModel
from app.core.repository.BaseRepository import BaseRepository


class RoteiroRepository(BaseRepository[RoteiroModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RoteiroModel)
