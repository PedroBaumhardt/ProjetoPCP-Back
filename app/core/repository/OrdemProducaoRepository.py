from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.OrdemProducaoModel import OrdemProducaoModel
from app.core.repository.BaseRepository import BaseRepository


class OrdemProducaoRepository(BaseRepository[OrdemProducaoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrdemProducaoModel)

    # -- maior sequencia_programacao entre todas as ordens (None se a tabela estiver vazia)
    async def get_highest_sequencia_programacao(self) -> int | None:
        result = await self.session.execute(select(func.max(OrdemProducaoModel.sequencia_programacao)))
        return result.scalar_one_or_none()

    # -- maior data_fim_prevista entre todas as ordens (None se a tabela estiver vazia)
    async def get_higher_data_fim_prevista(self) -> date | None:
        result = await self.session.execute(select(func.max(OrdemProducaoModel.data_fim_prevista)))
        return result.scalar_one_or_none()
