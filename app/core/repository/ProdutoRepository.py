from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.ProdutoModel import ProdutoModel
from app.core.model.RoteiroModel import RoteiroModel
from app.core.model.PassoRoteiroModel import PassoRoteiroModel
from app.core.repository.BaseRepository import BaseRepository


class ProdutoRepository(BaseRepository[ProdutoModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProdutoModel)


    async def get_production_time_by_code(self, codigo: str) -> float | None:
        qry = (
            select(func.coalesce(func.sum(PassoRoteiroModel.tempo_unitario_min), 0.0))
            .select_from(ProdutoModel)
            .outerjoin(RoteiroModel, RoteiroModel.produto_id == ProdutoModel.id)
            .outerjoin(PassoRoteiroModel, PassoRoteiroModel.roteiro_id == RoteiroModel.id)
            .where(ProdutoModel.codigo == codigo)
            .group_by(ProdutoModel.id)
        )
        result = await self.session.execute(qry)
        return result.scalar_one_or_none()
