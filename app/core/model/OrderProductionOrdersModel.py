import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.OrderModel import OrderModel
    from app.core.model.ProductionOrderModel import ProductionOrderModel


class OrderProductionOrdersModel(BaseModel):
    __tablename__ = "order_production_orders"

    # Columns
    quantity: Mapped[float]
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id")
    )
    production_order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("production_orders.id")
    )


    # Relationships
    order: Mapped["OrderModel"] = relationship(back_populates="order_production_orders")
    production_order: Mapped["ProductionOrderModel"] = relationship(back_populates="order_production_orders")