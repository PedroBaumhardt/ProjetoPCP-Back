from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.RecipeStepModel import RecipeStepModel
from app.core.repository.BaseRepository import BaseRepository


class RecipeStepRepository(BaseRepository[RecipeStepModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RecipeStepModel)
