from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.model.BaseModel import BaseModel


class RecursoModel(BaseModel):
    __tablename__ = "recursos"

    codigo:              Mapped[str]   = mapped_column(String(10), unique=True, nullable=False)
    descricao:           Mapped[str]   = mapped_column(String(255), nullable=False)
    tipo:                Mapped[str]   = mapped_column(String(20), nullable=False)
    capacidade_horas_dia: Mapped[float] = mapped_column(Float, nullable=False)
    status:              Mapped[str]   = mapped_column(String(20), nullable=False)
