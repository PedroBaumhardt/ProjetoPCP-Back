# -- controller de importacao delegando ao service

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.service.ImportService import ImportService


class ImportController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = ImportService(session)

    async def import_recursos(self, content: bytes) -> int:
        return await self.service.import_recursos(content)

    async def import_materiais(self, content: bytes) -> int:
        return await self.service.import_materiais(content)

    async def import_clientes(self, content: bytes) -> int:
        return await self.service.import_clientes(content)

    async def import_produtos(self, content: bytes) -> int:
        return await self.service.import_produtos(content)

    async def import_estoque(self, content: bytes) -> int:
        return await self.service.import_estoque(content)

    async def import_roteiros(self, content: bytes) -> int:
        return await self.service.import_roteiros(content)

    async def import_passos_roteiro(self, content: bytes) -> int:
        return await self.service.import_passos_roteiro(content)

    async def import_estruturas_produto(self, content: bytes) -> int:
        return await self.service.import_estruturas_produto(content)

    async def import_componentes(self, content: bytes) -> int:
        return await self.service.import_componentes(content)

    async def import_pedidos(self, content: bytes) -> int:
        return await self.service.import_pedidos(content)

    async def import_ordens_producao(self, content: bytes) -> int:
        return await self.service.import_ordens_producao(content)
