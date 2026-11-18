from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model.RecipeStepOutputModel import RecipeStepOutputModel
from app.core.repository.BaseRepository import BaseRepository


class RecipeStepOutputRepository(BaseRepository[RecipeStepOutputModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RecipeStepOutputModel)
