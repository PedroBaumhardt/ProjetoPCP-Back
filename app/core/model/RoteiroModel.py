import uuid

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.ProdutoModel import ProdutoModel
    from app.core.model.PassoRoteiroModel import PassoRoteiroModel


class RoteiroModel(BaseModel):
    __tablename__ = "roteiros"

    produto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("produtos.id"), unique=True, nullable=False
    )

    produto_rel: Mapped["ProdutoModel"] = relationship(back_populates="roteiro")
    passos: Mapped[list["PassoRoteiroModel"]] = relationship(
        back_populates="roteiro_rel", cascade="all, delete-orphan"
    )
