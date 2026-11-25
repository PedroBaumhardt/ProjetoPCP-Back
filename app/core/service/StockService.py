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
        material = await self.material_repository.get_by_id(uuid.UUID(material_id))
        if not material:
            raise ValueError("Material not found")
        results = await self.repository.get_by_field_in("material_codigo", [material.codigo])
        if not results:
            raise ValueError("Stock not found")
        return results[0].to_dict()
