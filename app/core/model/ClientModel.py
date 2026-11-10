from sqlalchemy.orm import Mapped, mapped_column, Relationship
from sqlalchemy import String

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.OrderModel import OrderModel

class ClientModel(BaseModel):
    __tablename__ = "clients"

    # Columns
    name: Mapped[str] = mapped_column( String(255) )

    # Relationships
    orders: Mapped[list["OrderModel"]] = Relationship(
        back_populates="client",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )