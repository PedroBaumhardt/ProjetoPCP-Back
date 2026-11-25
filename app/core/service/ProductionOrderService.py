import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import OrdemProducaoModel
from app.core.repository import OrdemProducaoRepository
from app.core.service import BaseService


class ProductionOrderService(BaseService[OrdemProducaoModel]):
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
        mdl.priority = priority
        await self.repository.update(mdl)