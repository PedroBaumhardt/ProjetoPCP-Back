from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.RecipeStepInputModel import RecipeStepInputModel
from app.core.repository.BaseRepository import BaseRepository


class RecipeStepInputRepository(BaseRepository[RecipeStepInputModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RecipeStepInputModel)
