from sqlalchemy.ext.asyncio import AsyncSession

from app.core.controller import BaseController
from app.core.service.ProductStructureService import ProductStructureService


class ProductStructureController(BaseController[ProductStructureService]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProductStructureService(session))

    async def get_all(self) -> list[dict]:
        data = await self.service.get_all()
        return data

    async def get_by_id(self, id: str) -> dict:
        data = await self.service.get_by_id(id)
        return data
