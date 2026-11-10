import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.RecipeStepModel import RecipeStepModel


class StepModel(BaseModel):
    __tablename__ = "steps"

    # Columns
    name: Mapped[str] = mapped_column( String(255) )
    current_recipe_step_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipe_steps.id", ondelete="SET NULL", use_alter=True),
        unique=True,
        nullable=True,
    )

    # Relationships
    current_recipe_step: Mapped["RecipeStepModel | None"] = Relationship(
        back_populates="current_step",
        foreign_keys=[current_recipe_step_id],
        post_update=True,
    )
    recipe_steps: Mapped[list["RecipeStepModel"]] = Relationship(
        back_populates="step",
        foreign_keys="RecipeStepModel.step_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )