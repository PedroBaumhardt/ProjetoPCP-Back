import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import MaterialModel
from app.core.repository import MaterialRepository
from app.core.service import BaseService


class MaterialService(BaseService[MaterialModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(MaterialRepository(session))

    async def get_all(self) -> list[dict]:
        data = await self.repository.get_all()
        dict_data = []
        for item in data:
            dict_data.append(item.to_dict())
        return dict_data

    async def get_by_id(self, id: str) -> dict:
        data = await self.repository.get_by_id(uuid.UUID(id))
        if not data:
            raise ValueError("Material not found")
        return data.to_dict()
