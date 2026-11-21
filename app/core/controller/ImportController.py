from typing import TypeVar

from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.controller.BaseController import BaseController
from app.core.schema.ImportSchema import (
    ProdutoImportList,
    MaterialImportList,
    EstruturaProdutoImportList,
    EstoqueImportList,
    RecursoImportList,
    PedidoImportList,
    OrdemProducaoImportList,
)
from app.core.service.ImportService import ImportService

SchemaType = TypeVar("SchemaType")


class ImportController(BaseController[ImportService]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ImportService(session))

    # -- le o arquivo json (raiz = array) e valida cada item contra o schema
    @staticmethod
    def _parse(content: bytes, adapter: TypeAdapter[list[SchemaType]]) -> list[SchemaType]:
        return adapter.validate_json(content)

    # -- garante que nao ha codigo repetido dentro do arquivo
    @staticmethod
    def _check_unique(values: list[str], label: str) -> None:
        seen, duplicated = set(), set()
        for value in values:
            (duplicated if value in seen else seen).add(value)
        if duplicated:
            raise ValueError(f"{label} repetido no arquivo: {', '.join(sorted(duplicated))}")

    async def import_recursos(self, content: bytes) -> int:
        items = self._parse(content, RecursoImportList)
        self._check_unique([i.codigo for i in items], "codigo de recurso")
        return await self.service.import_recursos(items)

    async def import_materiais(self, content: bytes) -> int:
        items = self._parse(content, MaterialImportList)
        self._check_unique([i.codigo for i in items], "codigo de material")
        return await self.service.import_materiais(items)

    async def import_produtos(self, content: bytes) -> int:
        items = self._parse(content, ProdutoImportList)
        self._check_unique([i.codigo for i in items], "codigo de produto")
        return await self.service.import_produtos(items)

    async def import_estruturas_produto(self, content: bytes) -> int:
        items = self._parse(content, EstruturaProdutoImportList)
        self._check_unique([i.produto for i in items], "produto")
        return await self.service.import_estruturas_produto(items)

    async def import_estoque(self, content: bytes) -> int:
        items = self._parse(content, EstoqueImportList)
        self._check_unique([i.material for i in items], "material")
        return await self.service.import_estoque(items)

    async def import_pedidos(self, content: bytes) -> int:
        items = self._parse(content, PedidoImportList)
        self._check_unique([i.numero for i in items], "numero de pedido")
        return await self.service.import_pedidos(items)

    async def import_ordens_producao(self, content: bytes) -> int:
        items = self._parse(content, OrdemProducaoImportList)
        self._check_unique([i.numero for i in items], "numero de ordem")
        return await self.service.import_ordens_producao(items)
