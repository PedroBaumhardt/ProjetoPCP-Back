from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.PedidoModel import PedidoModel


class ClienteModel(BaseModel):
    __tablename__ = "clientes"

    nome:     Mapped[str] = mapped_column(String(255), nullable=False)
    email:    Mapped[str] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str] = mapped_column(String(50), nullable=True)

    pedidos: Mapped[list["PedidoModel"]] = relationship(back_populates="cliente_rel")
