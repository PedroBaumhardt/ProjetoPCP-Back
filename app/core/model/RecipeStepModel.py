import uuid
from typing import Any

from sqlalchemy import Text, CheckConstraint, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from app.core.model.BaseModel import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.model.RecipeModel import RecipeModel
    from app.core.model.StepModel import StepModel
    from app.core.model.RecipeStepInputModel import RecipeStepInputModel
    from app.core.model.RecipeStepOutputModel import RecipeStepOutputModel
    from app.core.model.OrderModel import OrderModel


class RecipeStepModel(BaseModel):
    __tablename__ = "recipe_steps"
    __table_args__ = (
        CheckConstraint("estimated_time >= 0", name="estimated_time_non_negative"),
        CheckConstraint("step_number >= 0", name="step_number_non_negative"),
    )

    # Columns
    recipe_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE")
    )
    step_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("steps.id", ondelete="CASCADE")
    )
    description: Mapped[str] = mapped_column( Text )
    estimated_time: Mapped[int]
    step_number: Mapped[int]
    # MutableDict only tracks top-level changes (e.g. meta["x"] = 1).
    # Nested changes (e.g. meta["config"]["timeout"] = 5) are NOT detected and won't be saved.
    # For nested changes, reassign the top-level key or call
    # sqlalchemy.orm.attributes.flag_modified(obj, "meta").
    meta: Mapped[dict[str, Any]] = mapped_column(MutableDict.as_mutable(JSONB), default=dict)

    # Relationships
    recipe: Mapped["RecipeModel"]           = Relationship(back_populates="recipe_steps")
    step:   Mapped["StepModel"]             = Relationship(back_populates="recipe_steps", foreign_keys=[step_id])

    recipe_step_inputs: Mapped[list["RecipeStepInputModel"]] = Relationship(
        back_populates="recipe_step",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    recipe_step_outputs: Mapped[list["RecipeStepOutputModel"]] = Relationship(
        back_populates="recipe_step",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    current_step: Mapped["StepModel | None"] = Relationship(
        back_populates="current_recipe_step",
        foreign_keys="StepModel.current_recipe_step_id",
        post_update=True,
    )
    current_orders: Mapped[list["OrderModel"]] = Relationship(
        back_populates="current_recipe_step",
        foreign_keys="OrderModel.current_recipe_step_id",
    )
