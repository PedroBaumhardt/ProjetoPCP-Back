from sqlalchemy.ext.asyncio import AsyncSession

from app.core.controller import BaseController
from app.core.service.StockService import StockService


class StockController(BaseController[StockService]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(StockService(session))

    async def get_by_material_id(self, material_id: str) -> dict:
        data = await self.service.get_by_material_id(material_id)
        return data

    async def increase_by_material_id(self, material_id: str, quantity: int) -> None:
        await self.service.increase_by_material_id(material_id, quantity)