from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.model.BaseModel import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    # Columns
    nickname:        Mapped[str] = mapped_column(
        String(255),
        unique=True
    )
    hashed_password: Mapped[str] = mapped_column( String(255) )
    role:            Mapped[int]