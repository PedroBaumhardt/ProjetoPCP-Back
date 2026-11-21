from app.core.model.BaseModel import BaseModel
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(BaseModel):
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashpw: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[int] = mapped_column(Integer, default=0)