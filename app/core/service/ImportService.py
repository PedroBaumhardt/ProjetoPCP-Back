from typing import Awaitable, Callable

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
    ProdutoImport,
    MaterialImport,
    EstruturaProdutoImport,
    EstoqueImport,
    RecursoImport,
    PedidoImport,
    OrdemProducaoImport,
)


# -- service de importacao (dominio): recebe os schemas ja validados pelo controller,
# -- confere as referencias e regras que dependem do banco e persiste via repositories
# -- ordem esperada: recursos, materiais, produtos, estrutura_produtos, estoque, pedidos, ordens_producao

class ImportService:
    def __init__(self, session: AsyncSession) -> None:
        # -- a sessao fica no service so para controlar a transacao (commit/rollback)
        self.session = session
        self.resources = RecursoRepository(session)
        self.materials = MaterialRepository(session)
        self.products = ProdutoRepository(session)
        self.routings = RoteiroRepository(session)
        self.structures = EstruturaProdutoRepository(session)
        self.stock = EstoqueRepository(session)
        self.customers = ClienteRepository(session)
        self.sales_orders = PedidoRepository(session)
        self.production_orders = OrdemProducaoRepository(session)

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
    async def import_recursos(self, items: list[RecursoImport]) -> int:
        entities = [RecursoModel(**i.model_dump()) for i in items]
        await self._save(lambda: self.resources.create_many(entities))
        return len(items)

    # -- materiais.json
    async def import_materiais(self, items: list[MaterialImport]) -> int:
        entities = [MaterialModel(**i.model_dump()) for i in items]
        await self._save(lambda: self.materials.create_many(entities))
        return len(items)

    # -- produtos.json (produto + roteiro + passos)
    async def import_produtos(self, items: list[ProdutoImport]) -> int:
        resource_codes = {step.recurso for i in items for step in i.roteiro}
        await self._fetch_by(self.resources, "codigo", resource_codes, "recurso")

        products, routings = [], []
        for i in items:
            product = ProdutoModel(**i.model_dump(exclude={"roteiro"}))
            routing = RoteiroModel(produto_rel=product)
            routing.passos = [
                PassoRoteiroModel(
                    sequencia=step.sequencia,
                    recurso_codigo=step.recurso,
                    tempo_unitario_min=step.tempo_unitario_min,
                )
                for step in i.roteiro
            ]
            products.append(product)
            routings.append(routing)
        await self._save(
            lambda: self.products.create_many(products),
            lambda: self.routings.create_many(routings),
        )
        return len(items)

    # -- estrutura_produtos.json (estrutura + componentes)
    async def import_estruturas_produto(self, items: list[EstruturaProdutoImport]) -> int:
        products = await self._fetch_by(self.products, "codigo", {i.produto for i in items}, "produto")
        material_codes = {component.material for i in items for component in i.componentes}
        await self._fetch_by(self.materials, "codigo", material_codes, "material")

        entities = []
        for i in items:
            structure = EstruturaProdutoModel(produto_id=products[i.produto].id)
            structure.componentes = [
                ComponenteModel(
                    material_codigo=component.material,
                    quantidade=component.quantidade,
                    perda_percentual=component.perda_percentual,
                )
                for component in i.componentes
            ]
            entities.append(structure)
        await self._save(lambda: self.structures.create_many(entities))
        return len(items)

    # -- estoque.json
    async def import_estoque(self, items: list[EstoqueImport]) -> int:
        await self._fetch_by(self.materials, "codigo", {i.material for i in items}, "material")
        entities = [
            EstoqueModel(material_codigo=i.material, **i.model_dump(exclude={"material"}))
            for i in items
        ]
        await self._save(lambda: self.stock.create_many(entities))
        return len(items)

    # -- pedidos.json (cliente e criado pelo nome caso ainda nao exista)
    async def import_pedidos(self, items: list[PedidoImport]) -> int:
        products = await self._fetch_by(self.products, "codigo", {i.produto for i in items}, "produto")
        inactive = sorted({i.produto for i in items if not products[i.produto].ativo})
        if inactive:
            raise ValueError(f"pedido para produto inativo: {', '.join(inactive)}")

        names = {i.cliente for i in items}
        customers = {customer.nome: customer for customer in await self.customers.get_by_field_in("nome", names)}
        new_customers = [ClienteModel(nome=name) for name in sorted(names - customers.keys())]
        customers.update({customer.nome: customer for customer in new_customers})

        entities = [
            PedidoModel(
                cliente_rel=customers[i.cliente],
                produto_codigo=i.produto,
                **i.model_dump(exclude={"cliente", "produto"}),
            )
            for i in items
        ]
        await self._save(
            lambda: self.customers.create_many(new_customers),
            lambda: self.sales_orders.create_many(entities),
        )
        return len(items)

    # -- ordens_producao.json
    async def import_ordens_producao(self, items: list[OrdemProducaoImport]) -> int:
        products = await self._fetch_by(self.products, "codigo", {i.produto for i in items}, "produto")
        sales_orders = await self._fetch_by(
            self.sales_orders, "numero", {i.pedido for i in items if i.pedido}, "pedido"
        )

        for i in items:
            if i.quantidade_planejada < products[i.produto].lote_minimo:
                raise ValueError(f"ordem '{i.numero}' com quantidade_planejada abaixo do lote_minimo")
            if i.pedido and sales_orders[i.pedido].produto_codigo != i.produto:
                raise ValueError(f"ordem '{i.numero}' de produto diferente do pedido '{i.pedido}'")

        entities = [
            OrdemProducaoModel(
                produto_codigo=i.produto,
                pedido_numero=i.pedido,
                **i.model_dump(exclude={"produto", "pedido"}),
            )
            for i in items
        ]
        await self._save(lambda: self.production_orders.create_many(entities))
        return len(items)
