import uuid

from sqlalchemy import CheckConstraint, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.model.RecipeStepModel import RecipeStepModel
    from app.core.model.ProductModel import ProductModel


class RecipeStepOutputModel(BaseModel):
    __tablename__ = "recipe_step_outputs"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_quantity_non_negative"),
    )

    # Columns
    recipe_step_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipe_steps.id", ondelete="CASCADE")
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE")
    )
    quantity: Mapped[float]

    # Relationships
    recipe_step: Mapped["RecipeStepModel"] = Relationship(back_populates="recipe_step_outputs")
    product: Mapped["ProductModel"] = Relationship(back_populates="recipe_step_outputs")