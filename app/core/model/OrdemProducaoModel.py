from datetime import date
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

if TYPE_CHECKING:
    from app.core.model.ProdutoModel import ProdutoModel
    from app.core.model.PedidoModel import PedidoModel


class OrdemProducaoModel(BaseModel):
    __tablename__ = "ordens_producao"

    numero:                Mapped[str]            = mapped_column(String(20), unique=True, nullable=False)
    produto_codigo:        Mapped[str]            = mapped_column(String(10), ForeignKey("produtos.codigo"), nullable=False)
    pedido_numero:         Mapped[Optional[str]]  = mapped_column(String(20), ForeignKey("pedidos.numero"), nullable=True)
    prioridade:            Mapped[str]            = mapped_column(String(10), nullable=False)
    sequencia_programacao: Mapped[int]            = mapped_column(Integer, nullable=False)
    quantidade_planejada:  Mapped[int]            = mapped_column(Integer, nullable=False)
    quantidade_produzida:  Mapped[int]            = mapped_column(Integer, nullable=False, default=0)
    data_emissao:          Mapped[date]           = mapped_column(Date, nullable=False)
    data_inicio_prevista:  Mapped[date]           = mapped_column(Date, nullable=False)
    data_fim_prevista:     Mapped[date]           = mapped_column(Date, nullable=False)
    data_conclusao:        Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status:                Mapped[str]            = mapped_column(String(20), nullable=False)
    observacao:            Mapped[Optional[str]]  = mapped_column(String(500), nullable=True)

    produto_rel: Mapped["ProdutoModel"] = relationship()
    pedido_rel:  Mapped[Optional["PedidoModel"]] = relationship()
