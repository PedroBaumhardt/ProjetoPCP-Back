import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Float, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

if TYPE_CHECKING:
    from app.core.model.EstruturaProdutoModel import EstruturaProdutoModel
    from app.core.model.MaterialModel import MaterialModel


class ComponenteModel(BaseModel):
    __tablename__ = "componentes"

    estrutura_id:    Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("estrutura_produtos.id"), nullable=False)
    material_codigo: Mapped[str]             = mapped_column(String(10), ForeignKey("materiais.codigo"), nullable=False)
    quantidade:      Mapped[float]           = mapped_column(Float, nullable=False)
    perda_percentual: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    estrutura_rel: Mapped["EstruturaProdutoModel"] = relationship(back_populates="componentes")
    material_rel:  Mapped["MaterialModel"]         = relationship()
