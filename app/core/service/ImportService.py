import csv
import io
from datetime import date

from sqlalchemy import select
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


# -- helpers de parse ---------------------------------------------------------

def _parse_csv_text(content: bytes) -> list[dict[str, str]]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text), delimiter=";")
    return [row for row in reader]


def _date(value: str) -> date:
    return date.fromisoformat(value.strip())


def _int(value: str) -> int:
    return int(value.strip())


def _float(value: str) -> float:
    return float(value.strip().replace(",", "."))


def _bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "sim", "s")


def _str(value: str) -> str:
    return value.strip()


def _optional_str(value: str | None) -> str | None:
    if value is None or value.strip() == "":
        return None
    return value.strip()


def _optional_int(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    return int(value.strip())


def _optional_date(value: str | None) -> date | None:
    if value is None or value.strip() == "":
        return None
    return date.fromisoformat(value.strip())


# -- service de importacao (dominio) ------------------------------------------

class ImportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # -- metodo generico de persistencia
    async def _create(self, entity):
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    # -- busca auxiliar por campo
    async def _find_one(self, model, *filters):
        result = await self.session.execute(select(model).where(*filters))
        return result.scalar_one_or_none()

    # -- 1. Recurso
    async def import_recursos(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            obj = RecursoModel(
                codigo=_str(row["codigo"]),
                descricao=_str(row["descricao"]),
                tipo=_str(row["tipo"]),
                capacidade_horas_dia=_float(row["capacidade_horas_dia"]),
                status=_str(row["status"]),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 2. Material
    async def import_materiais(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            obj = MaterialModel(
                codigo=_str(row["codigo"]),
                descricao=_str(row["descricao"]),
                tipo=_str(row["tipo"]),
                unidade_medida=_str(row["unidade_medida"]),
                prazo_reposicao_dias=_optional_int(row.get("prazo_reposicao_dias")),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 3. Cliente
    async def import_clientes(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            obj = ClienteModel(
                nome=_str(row["nome"]),
                email=_optional_str(row.get("email")),
                telefone=_optional_str(row.get("telefone")),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 4. Produto
    async def import_produtos(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            obj = ProdutoModel(
                codigo=_str(row["codigo"]),
                descricao=_str(row["descricao"]),
                unidade_medida=_str(row["unidade_medida"]),
                lote_minimo=_int(row["lote_minimo"]),
                ativo=_bool(row.get("ativo", "true")),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 5. Estoque
    async def import_estoque(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            obj = EstoqueModel(
                material_codigo=_str(row["material_codigo"]),
                quantidade_disponivel=_float(row["quantidade_disponivel"]),
                quantidade_reservada=_float(row["quantidade_reservada"]),
                estoque_minimo=_float(row["estoque_minimo"]),
                data_atualizacao=_date(row["data_atualizacao"]),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 6. Roteiro (cabecalho)
    async def import_roteiros(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            produto_codigo = _str(row["produto_codigo"])
            produto = await self._find_one(ProdutoModel, ProdutoModel.codigo == produto_codigo)
            if produto is None:
                raise ValueError(f"Produto '{produto_codigo}' não encontrado")
            obj = RoteiroModel(produto_id=produto.id)
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 7. Passo Roteiro
    async def import_passos_roteiro(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            produto_codigo = _str(row["produto_codigo"])
            result = await self.session.execute(
                select(RoteiroModel)
                .join(ProdutoModel, RoteiroModel.produto_id == ProdutoModel.id)
                .where(ProdutoModel.codigo == produto_codigo)
            )
            roteiro = result.scalar_one_or_none()
            if roteiro is None:
                raise ValueError(f"Roteiro do produto '{produto_codigo}' não encontrado")
            obj = PassoRoteiroModel(
                roteiro_id=roteiro.id,
                sequencia=_int(row["sequencia"]),
                recurso_codigo=_str(row["recurso_codigo"]),
                tempo_unitario_min=_float(row["tempo_unitario_min"]),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 8. Estrutura Produto (cabecalho)
    async def import_estruturas_produto(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            produto_codigo = _str(row["produto_codigo"])
            produto = await self._find_one(ProdutoModel, ProdutoModel.codigo == produto_codigo)
            if produto is None:
                raise ValueError(f"Produto '{produto_codigo}' não encontrado")
            obj = EstruturaProdutoModel(produto_id=produto.id)
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 9. Componente
    async def import_componentes(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            produto_codigo = _str(row["produto_codigo"])
            result = await self.session.execute(
                select(EstruturaProdutoModel)
                .join(ProdutoModel, EstruturaProdutoModel.produto_id == ProdutoModel.id)
                .where(ProdutoModel.codigo == produto_codigo)
            )
            estrutura = result.scalar_one_or_none()
            if estrutura is None:
                raise ValueError(f"Estrutura do produto '{produto_codigo}' não encontrada")
            obj = ComponenteModel(
                estrutura_id=estrutura.id,
                material_codigo=_str(row["material_codigo"]),
                quantidade=_float(row["quantidade"]),
                perda_percentual=_float(row.get("perda_percentual", "0")),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 10. Pedido
    async def import_pedidos(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            cliente_nome = _str(row["cliente_nome"])
            cliente = await self._find_one(ClienteModel, ClienteModel.nome == cliente_nome)
            if cliente is None:
                raise ValueError(f"Cliente '{cliente_nome}' não encontrado")
            obj = PedidoModel(
                numero=_str(row["numero"]),
                cliente_id=cliente.id,
                produto_codigo=_str(row["produto_codigo"]),
                quantidade=_int(row["quantidade"]),
                data_pedido=_date(row["data_pedido"]),
                data_entrega=_date(row["data_entrega"]),
                prioridade=_str(row["prioridade"]),
                status=_str(row["status"]),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count

    # -- 11. Ordem de Producao
    async def import_ordens_producao(self, content: bytes) -> int:
        rows = _parse_csv_text(content)
        count = 0
        for row in rows:
            obj = OrdemProducaoModel(
                numero=_str(row["numero"]),
                produto_codigo=_str(row["produto_codigo"]),
                pedido_numero=_optional_str(row.get("pedido_numero")),
                prioridade=_str(row["prioridade"]),
                sequencia_programacao=_int(row["sequencia_programacao"]),
                quantidade_planejada=_int(row["quantidade_planejada"]),
                quantidade_produzida=_int(row.get("quantidade_produzida", "0")),
                data_inicio=_date(row["data_inicio"]),
                data_fim=_date(row["data_fim"]),
                data_criacao=_date(row["data_criacao"]),
                status=_str(row["status"]),
                observacao=_optional_str(row.get("observacao")),
            )
            await self._create(obj)
            count += 1
        await self.session.commit()
        return count
