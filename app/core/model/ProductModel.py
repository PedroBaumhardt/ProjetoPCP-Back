import uuid

from sqlalchemy import CheckConstraint, String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.OrderModel import OrderModel
    from app.core.model.RecipeStepInputModel import RecipeStepInputModel
    from app.core.model.RecipeStepOutputModel import RecipeStepOutputModel
    from app.core.model.RecipeModel import RecipeModel


class ProductModel(BaseModel):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="quantity_non_negative"),
    )

    # Columns
    name: Mapped[str] = mapped_column( String(255) )
    quantity: Mapped[int]
    recipe_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )

    # Relationships
    recipe: Mapped["RecipeModel | None"] = relationship(back_populates="product")
    orders: Mapped[list["OrderModel"]]   = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    recipe_step_inputs: Mapped[list["RecipeStepInputModel"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    recipe_step_outputs: Mapped[list["RecipeStepOutputModel"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )