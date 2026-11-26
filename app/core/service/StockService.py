import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import EstoqueModel
from app.core.repository import EstoqueRepository
from app.core.repository.MaterialRepository import MaterialRepository
from app.core.service import BaseService


class StockService(BaseService[EstoqueModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(EstoqueRepository(session))
        self.material_repository = MaterialRepository(session)

    async def get_by_material_id(self, material_id: str) -> dict:
        return (await self._get_model_by_material_id(material_id)).to_dict()

    async def _get_model_by_material_id(self, material_id: str) -> EstoqueModel:
        material = await self.material_repository.get_by_id(uuid.UUID(material_id))
        if not material:
            raise ValueError("Material not found")
        results = await self.repository.get_by_field_in("material_codigo", [material.codigo])
        if not results:
            raise ValueError("Stock not found")
        return results[0]

    async def increase_by_material_id(self, material_id: str, quantity: int) -> None:
        stock = await self._get_model_by_material_id(material_id)
        stock.quantidade_disponivel += quantity
        await self.repository.update(stock)

    async def reserve_by_material_id(self, material_id: str, quantity: int) -> None:
        stock = await self._get_model_by_material_id(material_id)
        stock.quantidade_reservada += quantity
        if stock.quantidade_disponivel < stock.quantidade_reservada:
            raise ValueError("Not enough stock available")

        await self.repository.update(stock)