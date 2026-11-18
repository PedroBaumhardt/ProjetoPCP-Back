from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.PassoRoteiroModel import PassoRoteiroModel
from app.core.repository.BaseRepository import BaseRepository


class PassoRoteiroRepository(BaseRepository[PassoRoteiroModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PassoRoteiroModel)
