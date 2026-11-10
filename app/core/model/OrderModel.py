import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.ClientModel import ClientModel
    from app.core.model.ProductModel import ProductModel
    from app.core.model.RecipeStepModel import RecipeStepModel

class OrderModel(BaseModel):
    __tablename__ = "orders"

    # Columns
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE")
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE")
    )
    quantity: Mapped[float]
    status: Mapped[int]
    line_number: Mapped[int] = mapped_column( unique=True )
    deadline: Mapped[datetime]
    current_recipe_step_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipe_steps.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    client: Mapped["ClientModel"] = relationship(back_populates="orders")
    product: Mapped["ProductModel"] = relationship(back_populates="orders")
    current_recipe_step: Mapped["RecipeStepModel | None"] = relationship(
        back_populates="current_orders",
        foreign_keys=[current_recipe_step_id],
    )