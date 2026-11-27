from sqlalchemy.ext.asyncio import AsyncSession

from app.core.controller import BaseController
from app.core.service.ProductionOrderService import ProductionOrderService
from app.core.schema.ProductionOrderSchema import ProductionOrderSchema

class ProductionOrderController(BaseController[ProductionOrderService]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProductionOrderService(session))

    async def get_all(self) -> list[dict]:
        data = await self.service.get_all()
        return data

    async def get_by_id(self, id: str) -> dict:
        data = await self.service.get_by_id(id)
        return data

    async def update_priority(self, id: str, priority: str) -> None:
        await self.service.update_priority(id, priority)

    async def create(self, prod_order: ProductionOrderSchema) -> None:
        await self.service.create(
            numero=prod_order.code,
            prioridade=prod_order.priority_str(),
            produto_codigo=prod_order.product,
            quantidade_planejada=prod_order.quantity,
            data_inicio_prevista=prod_order.estimated_start,
            observacao=prod_order.observation,
        )

    async def start(self, id: str) -> None:
        await self.service.start(id)

    async def cancel(self, id: str) -> None:
        await self.service.cancel(id)

    async def update_sequence_number(self, id: str, new_seq_number: int) -> None:
        await self.service.update_sequence_number(id, new_seq_number)