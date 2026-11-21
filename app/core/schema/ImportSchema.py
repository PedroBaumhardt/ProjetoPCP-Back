from datetime import date
from typing import Literal, Annotated

from pydantic import BaseModel, Field, TypeAdapter, model_validator

ProductCode = Annotated[str, Field(pattern=r"^P\d{3}$")]
MaterialCode = Annotated[str, Field(pattern=r"^M\d{3}$")]
ResourceCode = Annotated[str, Field(pattern=r"^R\d{2}$")]
SalesOrderNumber = Annotated[str, Field(pattern=r"^PED-\d{4}$")]
ProductionOrderNumber = Annotated[str, Field(pattern=r"^OP-\d{4}$")]

# -- mesmo tamanho das colunas String(n) dos models, para nao estourar no banco
Text255 = Annotated[str, Field(max_length=255)]
Text500 = Annotated[str, Field(max_length=500)]

Priority = Literal["alta", "normal", "baixa"]


# -- 1. produtos.json ---------------------------------------------------------

class PassoRoteiroImport(BaseModel):
    sequencia: int = Field(ge=1)
    recurso: ResourceCode
    tempo_unitario_min: float = Field(gt=0)


class ProdutoImport(BaseModel):
    codigo: ProductCode
    descricao: Text255
    unidade_medida: Literal["UN", "CJ", "KG", "M", "L"]
    lote_minimo: int = Field(ge=1)
    ativo: bool
    roteiro: list[PassoRoteiroImport] = Field(min_length=1)


# -- 2. materiais.json --------------------------------------------------------

class MaterialImport(BaseModel):
    codigo: MaterialCode
    descricao: Text255
    tipo: Literal["materia_prima", "componente", "embalagem"]
    unidade_medida: Literal["UN", "KG", "G", "M", "M2", "L"]
    prazo_reposicao_dias: int | None = Field(default=None, ge=0)


# -- 3. estrutura_produtos.json -----------------------------------------------

class ComponenteImport(BaseModel):
    material: MaterialCode
    quantidade: float = Field(gt=0)
    perda_percentual: float | None = Field(default=None, ge=0, le=100)


class EstruturaProdutoImport(BaseModel):
    produto: ProductCode
    componentes: list[ComponenteImport] = Field(min_length=1)

    @model_validator(mode="after")
    def _check_unique_materials(self):
        materials = [component.material for component in self.componentes]
        if len(materials) != len(set(materials)):
            raise ValueError(f"material repetido na estrutura do produto '{self.produto}'")
        return self


# -- 4. estoque.json ----------------------------------------------------------

class EstoqueImport(BaseModel):
    material: MaterialCode
    quantidade_disponivel: float = Field(ge=0)
    quantidade_reservada: float = Field(ge=0)
    estoque_minimo: float = Field(ge=0)
    data_atualizacao: date

    @model_validator(mode="after")
    def _check_reserved_within_available(self):
        if self.quantidade_reservada > self.quantidade_disponivel:
            raise ValueError(f"quantidade_reservada maior que disponivel no material '{self.material}'")
        return self


# -- 5. recursos.json ---------------------------------------------------------

class RecursoImport(BaseModel):
    codigo: ResourceCode
    descricao: Text255
    tipo: Literal["maquina", "posto_manual", "equipe"]
    capacidade_horas_dia: float = Field(gt=0, le=24)
    status: Literal["disponivel", "manutencao", "inativo"]


# -- 6. pedidos.json ----------------------------------------------------------

class PedidoImport(BaseModel):
    numero: SalesOrderNumber
    cliente: Text255
    produto: ProductCode
    quantidade: int = Field(gt=0)
    data_pedido: date
    data_entrega: date
    prioridade: Priority
    status: Literal["pendente", "em_producao", "atendido", "cancelado"]

    @model_validator(mode="after")
    def _check_delivery_after_order(self):
        if self.data_entrega < self.data_pedido:
            raise ValueError(f"data_entrega anterior a data_pedido no pedido '{self.numero}'")
        return self


# -- 7. ordens_producao.json --------------------------------------------------

class OrdemProducaoImport(BaseModel):
    numero: ProductionOrderNumber
    produto: ProductCode
    pedido: SalesOrderNumber | None = None
    prioridade: Priority
    sequencia_programacao: int = Field(ge=1)
    quantidade_planejada: int = Field(gt=0)
    quantidade_produzida: int = Field(ge=0)
    data_emissao: date
    data_inicio_prevista: date
    data_fim_prevista: date
    data_conclusao: date | None = None
    status: Literal["planejada", "liberada", "em_producao", "concluida", "cancelada"]
    observacao: Text500 | None = None

    @model_validator(mode="after")
    def _check_order_rules(self):
        if self.data_inicio_prevista < self.data_emissao:
            raise ValueError(f"data_inicio_prevista anterior a data_emissao na ordem '{self.numero}'")
        if self.data_fim_prevista < self.data_inicio_prevista:
            raise ValueError(f"data_fim_prevista anterior a data_inicio_prevista na ordem '{self.numero}'")
        if self.status == "concluida":
            if self.data_conclusao is None or self.quantidade_produzida <= 0:
                raise ValueError(
                    f"ordem concluida '{self.numero}' exige data_conclusao e quantidade_produzida > 0"
                )
        elif self.data_conclusao is not None:
            raise ValueError(f"data_conclusao so pode ser informada em ordem concluida ('{self.numero}')")
        if self.status in ("planejada", "liberada") and self.quantidade_produzida != 0:
            raise ValueError(f"ordem '{self.numero}' {self.status} deve ter quantidade_produzida = 0")
        return self


# -- adapters dos arquivos (raiz = array de objetos), criados uma vez so

ProdutoImportList = TypeAdapter(list[ProdutoImport])
MaterialImportList = TypeAdapter(list[MaterialImport])
EstruturaProdutoImportList = TypeAdapter(list[EstruturaProdutoImport])
EstoqueImportList = TypeAdapter(list[EstoqueImport])
RecursoImportList = TypeAdapter(list[RecursoImport])
PedidoImportList = TypeAdapter(list[PedidoImport])
OrdemProducaoImportList = TypeAdapter(list[OrdemProducaoImport])
