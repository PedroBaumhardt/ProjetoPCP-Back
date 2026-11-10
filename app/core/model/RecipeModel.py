from sqlalchemy.orm import Mapped, relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.ProductModel import ProductModel
    from app.core.model.RecipeStepModel import RecipeStepModel


class RecipeModel(BaseModel):
    __tablename__ = "recipes"

    # Columns
    # N/A

    # Relationships
    product: Mapped["ProductModel | None"] = relationship(back_populates="recipe")
    recipe_steps: Mapped[list["RecipeStepModel"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )