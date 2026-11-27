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

    async def get_material_quantities_with_product_code(self, product_code: str) -> dict[str, float]:
        # Retorna {material_codigo: quantidade por unidade do produto, já com a perda}
        # Soma caso o material apareça mais de uma vez na estrutura
        mdl = await self.repository.get_by_product_code(product_code)
        if mdl is None:
            raise ValueError("Product structure not found")

        quantities: dict[str, float] = {}
        for item in mdl.componentes:
            loss = (item.perda_percentual or 0) / 100
            qty = item.quantidade * (1 + loss)
            quantities[item.material_codigo] = quantities.get(item.material_codigo, 0) + qty
        return quantities
