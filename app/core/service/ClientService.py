import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import ClienteModel
from app.core.repository import ClienteRepository
from app.core.service import BaseService


class ClientService(BaseService[ClienteModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(ClienteRepository(session))

    async def get_all(self) -> list[dict]:
        data = await self.repository.get_all()
        dict_data = []
        for item in data:
            dict_data.append(item.to_dict())
        return dict_data

    async def get_by_id(self, id: str) -> dict:
        data = await self.repository.get_by_id(uuid.UUID(id))
        if not data:
            raise ValueError("Client not found")
        return data.to_dict()
