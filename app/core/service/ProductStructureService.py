import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import EstruturaProdutoModel
from app.core.repository import EstruturaProdutoRepository
from app.core.service import BaseService


class ProductStructureService(BaseService[EstruturaProdutoModel]):
    repository: EstruturaProdutoRepository

    def __init__(self, session: AsyncSession):
        super().__init__(EstruturaProdutoRepository(session))

    async def get_all(self) -> list[dict]:
        data = await self.repository.get_all()
        dict_data = []
        for item in data:
            dict_data.append(item.to_dict())
        return dict_data

    async def get_by_id(self, id: str) -> dict:
        data = await self.repository.get_by_id(uuid.UUID(id))
        if not data:
            raise ValueError("Product structure not found")
        return data.to_dict()

    async def get_material_ids_with_product_id(self, product_id) -> list[str]:
        mdl = await self.repository.get_by_product_id(product_id)
        return [item.material_id for item in mdl.compomponentes]