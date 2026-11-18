from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.model.BaseModel import BaseModel


class MaterialModel(BaseModel):
    __tablename__ = "materiais"

    codigo:              Mapped[str]           = mapped_column(String(10), unique=True, nullable=False)
    descricao:           Mapped[str]           = mapped_column(String(255), nullable=False)
    tipo:                Mapped[str]           = mapped_column(String(20), nullable=False)
    unidade_medida:      Mapped[str]           = mapped_column(String(10), nullable=False)
    prazo_reposicao_dias: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
