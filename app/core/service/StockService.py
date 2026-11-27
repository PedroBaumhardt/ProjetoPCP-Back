import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import EstoqueModel
from app.core.repository import EstoqueRepository
from app.core.repository.MaterialRepository import MaterialRepository
from app.core.service import BaseService

_FLOAT_TOLERANCE = 1e-9


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
        return await self._get_model_by_material_code(material.codigo)

    async def _get_model_by_material_code(self, material_code: str) -> EstoqueModel:
        results = await self.repository.get_by_field_in("material_codigo", [material_code])
        if not results:
            raise ValueError("Stock not found")
        return results[0]

    async def increase_by_material_id(self, material_id: str, quantity: int) -> None:
        stock = await self._get_model_by_material_id(material_id)
        stock.quantidade_disponivel += quantity
        await self.repository.update(stock)

    async def reserve_by_material_code(self, material_code: str, quantity: float) -> None:
        stock = await self._get_model_by_material_code(material_code)
        stock.quantidade_reservada += quantity
        if stock.quantidade_disponivel < stock.quantidade_reservada:
            raise ValueError("Not enough stock available")

        await self.repository.update(stock)

    async def consume_reserved_by_material_code(self, material_code: str, quantity: float) -> None:
        # Material reservado sai do estoque: reservada já está contida na disponível, então desconta das duas
        stock = await self._get_model_by_material_code(material_code)
        # Tolerância para erro de arredondamento de float ao consumir a reserva aos poucos
        if stock.quantidade_reservada - quantity < -_FLOAT_TOLERANCE:
            raise ValueError("Not enough reserved stock")

        stock.quantidade_reservada = max(stock.quantidade_reservada - quantity, 0.0)
        stock.quantidade_disponivel -= quantity
        await self.repository.update(stock)
