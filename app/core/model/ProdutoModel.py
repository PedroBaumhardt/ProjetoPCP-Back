from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.RoteiroModel import RoteiroModel
    from app.core.model.EstruturaProdutoModel import EstruturaProdutoModel


class ProdutoModel(BaseModel):
    __tablename__ = "produtos"

    codigo:         Mapped[str]  = mapped_column(String(10), unique=True, nullable=False)
    descricao:      Mapped[str]  = mapped_column(String(255), nullable=False)
    unidade_medida: Mapped[str]  = mapped_column(String(10), nullable=False)
    lote_minimo:    Mapped[int]  = mapped_column(Integer, nullable=False)
    ativo:          Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    roteiro: Mapped["Optional[RoteiroModel]"] = relationship(
        back_populates="produto_rel", cascade="all, delete-orphan", uselist=False
    )
    estrutura: Mapped["EstruturaProdutoModel"] = relationship(
        back_populates="produto_rel", cascade="all, delete-orphan", uselist=False
    )
