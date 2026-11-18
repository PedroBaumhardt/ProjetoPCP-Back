import uuid

from sqlalchemy import String, Integer, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.RoteiroModel import RoteiroModel
    from app.core.model.RecursoModel import RecursoModel


class PassoRoteiroModel(BaseModel):
    __tablename__ = "passos_roteiro"

    roteiro_id:        Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roteiros.id"), nullable=False)
    sequencia:         Mapped[int]       = mapped_column(Integer, nullable=False)
    recurso_codigo:    Mapped[str]       = mapped_column(String(10), ForeignKey("recursos.codigo"), nullable=False)
    tempo_unitario_min: Mapped[float]    = mapped_column(Float, nullable=False)

    roteiro_rel: Mapped["RoteiroModel"] = relationship(back_populates="passos")
    recurso_rel: Mapped["RecursoModel"] = relationship()
