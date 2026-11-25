import datetime
import math
import uuid
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import OrdemProducaoModel
from app.core.repository import OrdemProducaoRepository
from app.core.service import BaseService
from app.core.service.ProductService import ProductService

_MINUTES_PER_DAY = 24 * 60

class ProductionOrderService(BaseService[OrdemProducaoModel]):
    repository: OrdemProducaoRepository

    def __init__(self, session: AsyncSession):
        super().__init__(OrdemProducaoRepository(session))

    async def get_all(self) -> list[dict]:
        data = await self.repository.get_all()
        dict_data = []
        for item in data:
            dict_data.append(item.to_dict())
        return dict_data

    async def get_by_id(self, id: str) -> dict:
        data = await self.repository.get_by_id(uuid.UUID(id))
        if not data:
            raise ValueError("Production order not found")
        return data.to_dict()

    async def update_priority(self, id: str, priority: str) -> None:
        mdl = await self.repository.get_by_id(uuid.UUID(id))
        if not mdl:
            raise ValueError("Production order not found")
        mdl.prioridade = priority
        await self.repository.update(mdl)

    async def create(self,
                     numero: str,
                     produto_codigo: str,
                     prioridade: str,
                     quantidade_planejada: int,
                     data_inicio_prevista: datetime.date,
                     data_emissao: datetime.date | None = None,
                     pedido_numero: str | None = None,
                     observacao: str | None = None,
                     ) -> None:
        initial_status = "liberada"
        if data_emissao is None:
            data_emissao = datetime.date.today()

        sequencia_programacao = await self.repository.get_highest_sequencia_programacao()
        if not sequencia_programacao:
            sequencia_programacao = -1
        sequencia_programacao += 1

        product_service = ProductService(self.repository.session)
        production_minutes = await product_service.get_production_time_by_code(produto_codigo)
        production_minutes *= quantidade_planejada
        production_days = math.ceil(production_minutes / _MINUTES_PER_DAY)

        current_highest_date = await self.repository.get_higher_data_fim_prevista()
        if not current_highest_date or current_highest_date < data_inicio_prevista:
            current_highest_date = data_inicio_prevista
        data_fim_prevista = current_highest_date + datetime.timedelta(days=production_days)

        status = initial_status
        quantidade_produzida = 0

        mdl = OrdemProducaoModel(
            numero=numero,
            produto_codigo=produto_codigo,
            pedido_numero=pedido_numero,
            prioridade=prioridade,
            sequencia_programacao=sequencia_programacao,
            quantidade_planejada=quantidade_planejada,
            quantidade_produzida=quantidade_produzida,
            data_emissao=data_emissao,
            data_inicio_prevista=data_inicio_prevista,
            data_fim_prevista=data_fim_prevista,
            status=status,
            observacao=observacao
        )
        await self.repository.create(mdl)