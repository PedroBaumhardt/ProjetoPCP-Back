from datetime import date
from typing import Sequence

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

    # -- ordens ordenadas por sequencia_programacao; se since for informado, apenas sequencia_programacao >= since
    async def get_all_sequence_ordered(self, since: int | None = None) -> Sequence[OrdemProducaoModel]:
        stmt = select(OrdemProducaoModel)
        if since is not None:
            stmt = stmt.where(OrdemProducaoModel.sequencia_programacao >= since)
        stmt = stmt.order_by(OrdemProducaoModel.sequencia_programacao)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # -- ordem com a sequencia_programacao informada (None se nao existir)
    # -- valores negativos (-1 = fora da sequencia) nao identificam uma ordem unica, entao retornam None
    async def get_by_sequence_num(self, sequence_num: int) -> OrdemProducaoModel | None:
        if sequence_num < 0:
            return None
        result = await self.session.execute(
            select(OrdemProducaoModel).where(OrdemProducaoModel.sequencia_programacao == sequence_num)
        )
        return result.scalar_one_or_none()
