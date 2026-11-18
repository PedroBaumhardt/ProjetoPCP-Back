from datetime import date

from sqlalchemy import String, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.MaterialModel import MaterialModel


class EstoqueModel(BaseModel):
    __tablename__ = "estoque"

    material_codigo:       Mapped[str]   = mapped_column(String(10), ForeignKey("materiais.codigo"), unique=True, nullable=False)
    quantidade_disponivel: Mapped[float] = mapped_column(Float, nullable=False)
    quantidade_reservada:  Mapped[float] = mapped_column(Float, nullable=False)
    estoque_minimo:        Mapped[float] = mapped_column(Float, nullable=False)
    data_atualizacao:      Mapped[date]  = mapped_column(Date, nullable=False)

    material_rel: Mapped["MaterialModel"] = relationship()
