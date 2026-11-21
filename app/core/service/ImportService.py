from typing import TypeVar, Awaitable, Callable

from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import (
    ProdutoModel,
    RoteiroModel,
    PassoRoteiroModel,
    MaterialModel,
    EstruturaProdutoModel,
    ComponenteModel,
    EstoqueModel,
    RecursoModel,
    ClienteModel,
    PedidoModel,
    OrdemProducaoModel,
)
from app.core.repository import (
    ProdutoRepository,
    RoteiroRepository,
    MaterialRepository,
    EstruturaProdutoRepository,
    EstoqueRepository,
    RecursoRepository,
    ClienteRepository,
    PedidoRepository,
    OrdemProducaoRepository,
)
from app.core.schema.ImportSchema import (
    ProdutoImportList,
    MaterialImportList,
    EstruturaProdutoImportList,
    EstoqueImportList,
    RecursoImportList,
    PedidoImportList,
    OrdemProducaoImportList,
)

SchemaType = TypeVar("SchemaType")


# -- service de importacao dos arquivos json (dominio)
# -- ordem esperada: recursos, materiais, produtos, estrutura_produtos, estoque, pedidos, ordens_producao

class ImportService:
    def __init__(self, session: AsyncSession) -> None:
        # -- a sessao fica no service so para controlar a transacao (commit/rollback)
        self.session = session
        self.recursos = RecursoRepository(session)
        self.materiais = MaterialRepository(session)
        self.produtos = ProdutoRepository(session)
        self.roteiros = RoteiroRepository(session)
        self.estruturas = EstruturaProdutoRepository(session)
        self.estoque = EstoqueRepository(session)
        self.clientes = ClienteRepository(session)
        self.pedidos = PedidoRepository(session)
        self.ordens = OrdemProducaoRepository(session)

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

    # -- busca registros pelo codigo e falha se algum referenciado nao existir
    @staticmethod
    async def _fetch_by(repository, field: str, codes: set[str], label: str) -> dict:
        found = {getattr(obj, field): obj for obj in await repository.get_by_field_in(field, codes)}
        missing = codes - found.keys()
        if missing:
            raise ValueError(f"{label} nao encontrado: {', '.join(sorted(missing))}")
        return found

    # -- executa as gravacoes via repositories numa transacao; conflitos (ex.: codigo ja importado) viram ValueError
    async def _save(self, *writes: Callable[[], Awaitable]) -> None:
        try:
            for write in writes:
                await write()
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"violacao de integridade: {e.orig}") from e

    # -- recursos.json
    async def import_recursos(self, content: bytes) -> int:
        items = self._parse(content, RecursoImportList)
        self._check_unique([i.codigo for i in items], "codigo de recurso")
        entities = [RecursoModel(**i.model_dump()) for i in items]
        await self._save(lambda: self.recursos.create_many(entities))
        return len(items)

    # -- materiais.json
    async def import_materiais(self, content: bytes) -> int:
        items = self._parse(content, MaterialImportList)
        self._check_unique([i.codigo for i in items], "codigo de material")
        entities = [MaterialModel(**i.model_dump()) for i in items]
        await self._save(lambda: self.materiais.create_many(entities))
        return len(items)

    # -- produtos.json (produto + roteiro + passos)
    async def import_produtos(self, content: bytes) -> int:
        items = self._parse(content, ProdutoImportList)
        self._check_unique([i.codigo for i in items], "codigo de produto")
        recursos = {passo.recurso for i in items for passo in i.roteiro}
        await self._fetch_by(self.recursos, "codigo", recursos, "recurso")

        produtos, roteiros = [], []
        for i in items:
            produto = ProdutoModel(**i.model_dump(exclude={"roteiro"}))
            roteiro = RoteiroModel(produto_rel=produto)
            roteiro.passos = [
                PassoRoteiroModel(
                    sequencia=passo.sequencia,
                    recurso_codigo=passo.recurso,
                    tempo_unitario_min=passo.tempo_unitario_min,
                )
                for passo in i.roteiro
            ]
            produtos.append(produto)
            roteiros.append(roteiro)
        await self._save(
            lambda: self.produtos.create_many(produtos),
            lambda: self.roteiros.create_many(roteiros),
        )
        return len(items)

    # -- estrutura_produtos.json (estrutura + componentes)
    async def import_estruturas_produto(self, content: bytes) -> int:
        items = self._parse(content, EstruturaProdutoImportList)
        self._check_unique([i.produto for i in items], "produto")
        produtos = await self._fetch_by(self.produtos, "codigo", {i.produto for i in items}, "produto")
        materiais = {componente.material for i in items for componente in i.componentes}
        await self._fetch_by(self.materiais, "codigo", materiais, "material")

        entities = []
        for i in items:
            estrutura = EstruturaProdutoModel(produto_id=produtos[i.produto].id)
            estrutura.componentes = [
                ComponenteModel(
                    material_codigo=componente.material,
                    quantidade=componente.quantidade,
                    perda_percentual=componente.perda_percentual or 0,
                )
                for componente in i.componentes
            ]
            entities.append(estrutura)
        await self._save(lambda: self.estruturas.create_many(entities))
        return len(items)

    # -- estoque.json
    async def import_estoque(self, content: bytes) -> int:
        items = self._parse(content, EstoqueImportList)
        self._check_unique([i.material for i in items], "material")
        await self._fetch_by(self.materiais, "codigo", {i.material for i in items}, "material")
        entities = [
            EstoqueModel(material_codigo=i.material, **i.model_dump(exclude={"material"}))
            for i in items
        ]
        await self._save(lambda: self.estoque.create_many(entities))
        return len(items)

    # -- pedidos.json (cliente e criado pelo nome caso ainda nao exista)
    async def import_pedidos(self, content: bytes) -> int:
        items = self._parse(content, PedidoImportList)
        self._check_unique([i.numero for i in items], "numero de pedido")
        produtos = await self._fetch_by(self.produtos, "codigo", {i.produto for i in items}, "produto")
        inativos = sorted({i.produto for i in items if not produtos[i.produto].ativo})
        if inativos:
            raise ValueError(f"pedido para produto inativo: {', '.join(inativos)}")

        nomes = {i.cliente for i in items}
        clientes = {cliente.nome: cliente for cliente in await self.clientes.get_by_field_in("nome", nomes)}
        novos = [ClienteModel(nome=nome) for nome in sorted(nomes - clientes.keys())]
        clientes.update({cliente.nome: cliente for cliente in novos})

        entities = [
            PedidoModel(
                cliente_rel=clientes[i.cliente],
                produto_codigo=i.produto,
                **i.model_dump(exclude={"cliente", "produto"}),
            )
            for i in items
        ]
        await self._save(
            lambda: self.clientes.create_many(novos),
            lambda: self.pedidos.create_many(entities),
        )
        return len(items)

    # -- ordens_producao.json
    async def import_ordens_producao(self, content: bytes) -> int:
        items = self._parse(content, OrdemProducaoImportList)
        self._check_unique([i.numero for i in items], "numero de ordem")
        produtos = await self._fetch_by(self.produtos, "codigo", {i.produto for i in items}, "produto")
        pedidos = await self._fetch_by(
            self.pedidos, "numero", {i.pedido for i in items if i.pedido}, "pedido"
        )

        for i in items:
            if i.quantidade_planejada < produtos[i.produto].lote_minimo:
                raise ValueError(f"ordem '{i.numero}' com quantidade_planejada abaixo do lote_minimo")
            if i.pedido and pedidos[i.pedido].produto_codigo != i.produto:
                raise ValueError(f"ordem '{i.numero}' de produto diferente do pedido '{i.pedido}'")

        entities = [
            OrdemProducaoModel(
                produto_codigo=i.produto,
                pedido_numero=i.pedido,
                **i.model_dump(exclude={"produto", "pedido"}),
            )
            for i in items
        ]
        await self._save(lambda: self.ordens.create_many(entities))
        return len(items)
