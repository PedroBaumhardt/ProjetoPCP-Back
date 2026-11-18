from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.OrdemProducaoModel import OrdemProducaoModel
from app.core.repository.BaseRepository import BaseRepository


class OrdemProducaoRepository(BaseRepository[OrdemProducaoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrdemProducaoModel)
