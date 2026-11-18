import uuid
from datetime import date

from sqlalchemy import String, Integer, Date, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.ProdutoModel import ProdutoModel
    from app.core.model.ClienteModel import ClienteModel


class PedidoModel(BaseModel):
    __tablename__ = "pedidos"

    numero:       Mapped[str]  = mapped_column(String(20), unique=True, nullable=False)
    cliente_id:   Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    produto_codigo: Mapped[str] = mapped_column(String(10), ForeignKey("produtos.codigo"), nullable=False)
    quantidade:   Mapped[int]  = mapped_column(Integer, nullable=False)
    data_pedido:  Mapped[date] = mapped_column(Date, nullable=False)
    data_entrega: Mapped[date] = mapped_column(Date, nullable=False)
    prioridade:   Mapped[str]  = mapped_column(String(10), nullable=False)
    status:       Mapped[str]  = mapped_column(String(20), nullable=False)

    produto_rel: Mapped["ProdutoModel"] = relationship()
    cliente_rel: Mapped["ClienteModel"] = relationship(back_populates="pedidos")
