import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.ProductModel import ProductModel
    from app.core.model.RecipeStepModel import RecipeStepModel
    from app.core.model.OrderProductionOrdersModel import OrderProductionOrdersModel

class ProductionOrderModel(BaseModel):
    __tablename__ = "production_orders"

    # Columns
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
    product: Mapped["ProductModel"] = relationship(back_populates="production_orders")
    current_recipe_step: Mapped["RecipeStepModel | None"] = relationship(
        back_populates="current_production_orders",
        foreign_keys=[current_recipe_step_id],
    )
    order_production_orders: Mapped[list["OrderProductionOrdersModel"]] = relationship(back_populates="production_order")